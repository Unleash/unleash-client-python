# pylint: disable=invalid-name
import warnings
import random
import string
from datetime import datetime, timezone
from typing import Callable, Optional
from apscheduler.job import Job
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
from UnleashClient.api import register_client
from UnleashClient.periodic_tasks import fetch_and_load_features, aggregate_and_send_metrics
from UnleashClient.strategies import ApplicationHostname, Default, GradualRolloutRandom, \
    GradualRolloutSessionId, GradualRolloutUserId, UserWithId, RemoteAddress, FlexibleRollout
from UnleashClient.constants import METRIC_LAST_SENT_TIME, DISABLED_VARIATION, ETAG
from UnleashClient.loader import load_features
from .utils import LOGGER
from .deprecation_warnings import strategy_v2xx_deprecation_check
from .cache import BaseCache, FileCache

# pylint: disable=dangerous-default-value
class UnleashClient:
    """
    A client for the Unleash feature toggle system.

    :param url: URL of the unleash server, required.
    :param app_name: Name of the application using the unleash client, required.
    :param  environment: Name of the environment using the unleash client, optional & defaults to "default".
    :param instance_id: Unique identifier for unleash client instance, optional & defaults to "unleash-client-python"
    :param refresh_interval: Provisioning refresh interval in seconds, optional & defaults to 15 seconds
    :param refresh_jitter: Provisioning refresh interval jitter in seconds, optional & defaults to None
    :param metrics_interval: Metrics refresh interval in seconds, optional & defaults to 60 seconds
    :param metrics_jitter: Metrics refresh interval jitter in seconds, optional & defaults to None
    :param disable_metrics: Disables sending metrics to unleash server, optional & defaults to false.
    :param custom_headers: Default headers to send to unleash server, optional & defaults to empty.
    :param custom_options: Default requests parameters, optional & defaults to empty.  Can be used to skip SSL verification.
    :param custom_strategies: Dictionary of custom strategy names : custom strategy objects.
    :param cache_directory: Location of the cache directory. When unset, FCache will determine the location.
    :param verbose_log_level: Numerical log level (https://docs.python.org/3/library/logging.html#logging-levels) for cases where checking a feature flag fails.
    :param cache: Custom cache implementation that extends UnleashClient.cache.BaseCache.  When unset, UnleashClient will use Fcache.
    :param scheduler: Custom APScheduler object.  Use this if you want to customize jobstore or executors.  When unset, UnleashClient will create it's own scheduler.
    :param scheduler_executor: Name of APSCheduler executor to use if using a custom scheduler.
    """
    def __init__(self,
                 url: str,
                 app_name: str,
                 environment: str = "default",
                 instance_id: str = "unleash-client-python",
                 refresh_interval: int = 15,
                 refresh_jitter: Optional[int] = None,
                 metrics_interval: int = 60,
                 metrics_jitter: Optional[int] = None,
                 disable_metrics: bool = False,
                 disable_registration: bool = False,
                 custom_headers: Optional[dict] = None,
                 custom_options: Optional[dict] = None,
                 custom_strategies: Optional[dict] = None,
                 cache_directory: Optional[str] = None,
                 project_name: str = None,
                 verbose_log_level: int = 30,
                 cache: Optional[BaseCache] = None,
                 scheduler: Optional[BaseScheduler] = None,
                 scheduler_executor: Optional[str] = None) -> None:
        custom_headers = custom_headers or {}
        custom_options = custom_options or {}
        custom_strategies = custom_strategies or {}

        # Configuration
        self.unleash_url = url.rstrip('/')
        self.unleash_app_name = app_name
        self.unleash_environment = environment
        self.unleash_instance_id = instance_id
        self.unleash_refresh_interval = refresh_interval
        self.unleash_refresh_jitter = int(refresh_jitter) if refresh_jitter is not None else None
        self.unleash_metrics_interval = metrics_interval
        self.unleash_metrics_jitter = int(metrics_jitter) if metrics_jitter is not None else None
        self.unleash_disable_metrics = disable_metrics
        self.unleash_disable_registration = disable_registration
        self.unleash_custom_headers = custom_headers
        self.unleash_custom_options = custom_options
        self.unleash_static_context = {
            "appName": self.unleash_app_name,
            "environment": self.unleash_environment
        }
        self.unleash_project_name = project_name
        self.unleash_verbose_log_level = verbose_log_level

        # Class objects
        self.features: dict = {}
        self.fl_job: Job = None
        self.metric_job: Job = None

        self.cache = cache or FileCache(self.unleash_app_name, directory=cache_directory)
        self.cache.mset({
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: ''
        })
        self.unleash_bootstrapped = self.cache.bootstrapped

        # Scheduler bootstrapping
        # - Figure out the Unleash executor name.
        if scheduler and scheduler_executor:
            self.unleash_executor_name = scheduler_executor
        elif scheduler and not scheduler_executor:
            raise ValueError("If using a custom scheduler, you must specify a executor.")
        else:
            if not scheduler:
                LOGGER.warning("scheduler_executor should only be used with a custom scheduler.")

            self.unleash_executor_name = f"unleash_executor_{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

        # Set up the scheduler.
        if scheduler:
            self.unleash_scheduler = scheduler
        else:
            executors = {
                self.unleash_executor_name: ThreadPoolExecutor()
            }
            self.unleash_scheduler = BackgroundScheduler(executors=executors)

        # Mappings
        default_strategy_mapping = {
            "applicationHostname": ApplicationHostname,
            "default": Default,
            "gradualRolloutRandom": GradualRolloutRandom,
            "gradualRolloutSessionId": GradualRolloutSessionId,
            "gradualRolloutUserId": GradualRolloutUserId,
            "remoteAddress": RemoteAddress,
            "userWithId": UserWithId,
            "flexibleRollout": FlexibleRollout
        }

        if custom_strategies:
            strategy_v2xx_deprecation_check([x for x in custom_strategies.values()])  # pylint: disable=R1721

        self.strategy_mapping = {**custom_strategies, **default_strategy_mapping}

        # Client status
        self.is_initialized = False

        # Bootstrapping
        if self.unleash_bootstrapped:
            load_features(cache=self.cache, feature_toggles=self.features, strategy_mapping=self.strategy_mapping)

    def initialize_client(self, fetch_toggles: bool = True) -> None:
        """
        Initializes client and starts communication with central unleash server(s).

        This kicks off:

        * Client registration
        * Provisioning poll
        * Stats poll

        If `fetch_toggles` is `False`, feature toggle polling will be turned off
        and instead the client will only load features from the cache. This is
        usually used to cater the multi-process setups, e.g. Django, Celery,
        etc.

        This will raise an exception on registration if the URL is invalid. It is done automatically if called inside a context manager as in:

        .. code-block:: python

            with UnleashClient(
                url="https://foo.bar",
                app_name="myClient1",
                instance_id="myinstanceid"
                ) as client:
                pass
        """
        # Only perform initialization steps if client is not initialized.
        if not self.is_initialized:
            try:
                # Setup
                metrics_args = {
                    "url": self.unleash_url,
                    "app_name": self.unleash_app_name,
                    "instance_id": self.unleash_instance_id,
                    "custom_headers": self.unleash_custom_headers,
                    "custom_options": self.unleash_custom_options,
                    "features": self.features,
                    "cache": self.cache
                }

                # Register app
                if not self.unleash_disable_registration:
                    register_client(self.unleash_url, self.unleash_app_name, self.unleash_instance_id,
                                    self.unleash_metrics_interval, self.unleash_custom_headers,
                                    self.unleash_custom_options, self.strategy_mapping)

                if fetch_toggles:
                    job_args = {
                        "url": self.unleash_url,
                        "app_name": self.unleash_app_name,
                        "instance_id": self.unleash_instance_id,
                        "custom_headers": self.unleash_custom_headers,
                        "custom_options": self.unleash_custom_options,
                        "cache": self.cache,
                        "features": self.features,
                        "strategy_mapping": self.strategy_mapping,
                        "project": self.unleash_project_name,
                    }
                    job_func: Callable = fetch_and_load_features
                else:
                    job_args = {
                        "cache": self.cache,
                        "feature_toggles": self.features,
                        "strategy_mapping": self.strategy_mapping,
                    }
                    job_func = load_features

                job_func(**job_args)  # type: ignore
                # Start periodic jobs
                self.unleash_scheduler.start()
                self.fl_job = self.unleash_scheduler.add_job(job_func,
                                                     trigger=IntervalTrigger(
                                                         seconds=int(self.unleash_refresh_interval),
                                                         jitter=self.unleash_refresh_jitter,
                                                     ),
                                                     executor=self.unleash_executor_name,
                                                     kwargs=job_args)

                if not self.unleash_disable_metrics:
                    self.metric_job = self.unleash_scheduler.add_job(aggregate_and_send_metrics,
                                                             trigger=IntervalTrigger(
                                                                 seconds=int(self.unleash_metrics_interval),
                                                                 jitter=self.unleash_metrics_jitter,
                                                             ),
                                                             executor=self.unleash_executor_name,
                                                             kwargs=metrics_args)
            except Exception as excep:
                # Log exceptions during initialization.  is_initialized will remain false.
                LOGGER.warning("Exception during UnleashClient initialization: %s", excep)
                raise excep
            else:
                # Set is_iniialized to true if no exception is encountered.
                self.is_initialized = True
        else:
            warnings.warn("Attempted to initialize an Unleash Client instance that has already been initialized.")

    def destroy(self) -> None:
        """
        Gracefully shuts down the Unleash client by stopping jobs, stopping the scheduler, and deleting the cache.

        You shouldn't need this too much!
        """
        self.fl_job.remove()
        if self.metric_job:
            self.metric_job.remove()
        self.unleash_scheduler.shutdown()
        self.cache.destroy()

    @staticmethod
    def _get_fallback_value(fallback_function: Callable, feature_name: str, context: dict) -> bool:
        if fallback_function:
            fallback_value = fallback_function(feature_name, context)
        else:
            fallback_value = False

        return fallback_value

    # pylint: disable=broad-except
    def is_enabled(self,
                   feature_name: str,
                   context: Optional[dict] = None,
                   fallback_function: Callable = None) -> bool:
        """
        Checks if a feature toggle is enabled.

        Notes:

        * If client hasn't been initialized yet or an error occurs, flat will default to false.

        :param feature_name: Name of the feature
        :param context: Dictionary with context (e.g. IPs, email) for feature toggle.
        :param fallback_function: Allows users to provide a custom function to set default value.
        :return: Feature flag result
        """
        context = context or {}

        base_context = self.unleash_static_context.copy()
        # Update context with static values and allow context to override environment
        base_context.update(context)
        context = base_context

        if self.unleash_bootstrapped or self.is_initialized:
            try:
                return self.features[feature_name].is_enabled(context)
            except Exception as excep:
                LOGGER.log(self.unleash_verbose_log_level, "Returning default value for feature: %s", feature_name)
                LOGGER.log(self.unleash_verbose_log_level, "Error checking feature flag: %s", excep)
                return self._get_fallback_value(fallback_function, feature_name, context)
        else:
            LOGGER.log(self.unleash_verbose_log_level, "Returning default value for feature: %s", feature_name)
            LOGGER.log(self.unleash_verbose_log_level, "Attempted to get feature_flag %s, but client wasn't initialized!", feature_name)
            return self._get_fallback_value(fallback_function, feature_name, context)

    # pylint: disable=broad-except
    def get_variant(self,
                    feature_name: str,
                    context: Optional[dict] = None) -> dict:
        """
        Checks if a feature toggle is enabled.  If so, return variant.

        Notes:

        * If client hasn't been initialized yet or an error occurs, flat will default to false.

        :param feature_name: Name of the feature
        :param context: Dictionary with context (e.g. IPs, email) for feature toggle.
        :return: Variant and feature flag status.
        """
        context = context or {}
        context.update(self.unleash_static_context)

        if self.unleash_bootstrapped or self.is_initialized:
            try:
                return self.features[feature_name].get_variant(context)
            except Exception as excep:
                LOGGER.log(self.unleash_verbose_log_level, "Returning default flag/variation for feature: %s", feature_name)
                LOGGER.log(self.unleash_verbose_log_level, "Error checking feature flag variant: %s", excep)
                return DISABLED_VARIATION
        else:
            LOGGER.log(self.unleash_verbose_log_level, "Returning default flag/variation for feature: %s", feature_name)
            LOGGER.log(self.unleash_verbose_log_level, "Attempted to get feature flag/variation %s, but client wasn't initialized!", feature_name)
            return DISABLED_VARIATION

    def __enter__(self) -> "UnleashClient":
        self.initialize_client()
        return self

    def __exit__(self, *args, **kwargs):
        self.destroy()
        return False
