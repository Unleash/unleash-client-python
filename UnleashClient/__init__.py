from datetime import datetime
from fcache.cache import FileCache
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from UnleashClient.api import register_client
from UnleashClient.periodic_tasks import fetch_and_load_features, aggregate_and_send_metrics
from UnleashClient.strategies import ApplicationHostname, Default, GradualRolloutRandom, \
    GradualRolloutSessionId, GradualRolloutUserId, UserWithId, RemoteAddress
from .utils import LOGGER


# pylint: disable=dangerous-default-value
class UnleashClient():
    """
    Client implementation.
    """
    def __init__(self,
                 url: str,
                 app_name: str,
                 instance_id: str = "unleash-client-python",
                 refresh_interval: int = 15,
                 metrics_interval: int = 60,
                 disable_metrics: bool = False,
                 custom_headers: dict = {},
                 custom_strategies: dict = {}) -> None:
        """
        A client for the Unleash feature toggle system.

        :param url: URL of the unleash server, required.
        :param app_name: Name of the application using the unleash client, required.
        :param instance_id: Unique identifier for unleash client instance, optional & defaults to "unleash-client-python"
        :param refresh_interval: Provisioning refresh interval in ms, optional & defaults to 15 seconds
        :param metrics_interval: Metrics refresh interval in ms, optional & defaults to 60 seconds
        :param disable_metrics: Disables sending metrics to unleash server, optional & defaults to false.
        :param custom_headers: Default headers to send to unleash server, optional & defaults to empty.
        :param custom_strategies: Dictionary of custom strategy names : custom strategy objects
        """
        # Configuration
        self.unleash_url = url.rstrip('\\')
        self.unleash_app_name = app_name
        self.unleash_instance_id = instance_id
        self.unleash_refresh_interval = refresh_interval
        self.unleash_metrics_interval = metrics_interval
        self.unleash_disable_metrics = disable_metrics
        self.unleash_custom_headers = custom_headers

        # Class objects
        self.cache = FileCache(self.unleash_instance_id)
        self.features: dict = {}
        self.scheduler = BackgroundScheduler()
        self.fl_job: Job = None
        self.metric_job: Job = None
        self.metrics_last_sent_time = datetime.now()

        # Mappings
        default_strategy_mapping = {
            "applicationHostname": ApplicationHostname,
            "default": Default,
            "gradualRolloutRandom": GradualRolloutRandom,
            "gradualRolloutSessionId": GradualRolloutSessionId,
            "gradualRolloutUserId": GradualRolloutUserId,
            "remoteAddress": RemoteAddress,
            "userWithId": UserWithId
        }

        self.strategy_mapping = {**custom_strategies, **default_strategy_mapping}

        # Client status
        self.is_initialized = False

    def initialize_client(self) -> None:
        """
        Initializes client and starts communication with central unleash server(s).

        This kicks off:
        * Client registration
        * Provisioning poll
        * Stats poll

        :return:
        """
        # Setup
        fl_args = {
            "url": self.unleash_url,
            "app_name": self.unleash_app_name,
            "instance_id": self.unleash_instance_id,
            "custom_headers": self.unleash_custom_headers,
            "cache": self.cache,
            "features": self.features,
            "strategy_mapping": self.strategy_mapping
        }

        metrics_args = {
            "url": self.unleash_url,
            "app_name": self.unleash_app_name,
            "instance_id": self.unleash_instance_id,
            "custom_headers": self.unleash_custom_headers,
            "features": self.features,
            "last_sent": self.metrics_last_sent_time
        }

        # Register app
        register_client(self.unleash_url, self.unleash_app_name, self.unleash_instance_id,
                        self.unleash_metrics_interval, self.unleash_custom_headers, self.strategy_mapping)

        fetch_and_load_features(**fl_args)

        # Start periodic jobs
        self.scheduler.start()
        self.fl_job = self.scheduler.add_job(fetch_and_load_features,
                                             trigger=IntervalTrigger(seconds=int(self.unleash_refresh_interval)),
                                             kwargs=fl_args)

        self.metric_job = self.scheduler.add_job(aggregate_and_send_metrics,
                                                 trigger=IntervalTrigger(seconds=int(self.unleash_metrics_interval)),
                                                 kwargs=metrics_args)

        self.is_initialized = True

    def destroy(self):
        """
        Gracefully shuts down the Unleash client by stopping jobs, stopping the scheduler, and deleting the cache.

        You shouldn't need this too much!

        :return:
        """
        self.fl_job.remove()
        self.metric_job.remove()
        self.scheduler.shutdown()
        self.cache.delete()

    # pylint: disable=broad-except
    def is_enabled(self,
                   feature_name: str,
                   context: dict = {},
                   default_value: bool = False) -> bool:
        """
        Checks if a feature toggle is enabled.

        Notes:
        * If client hasn't been initialized yet or an error occurs, flat will default to false.

        :param feature_name: Name of the feature
        :param context: Dictionary with context (e.g. IPs, email) for feature toggle.
        :param default_value: Allows override of default value.
        :return: True/False
        """
        if self.is_initialized:
            try:
                return self.features[feature_name].is_enabled(context, default_value)
            except Exception as excep:
                LOGGER.warning("Returning default value for feature: %s", feature_name)
                LOGGER.warning("Error checking feature flag: %s", excep)
                return default_value
        else:
            LOGGER.warning("Returning default value for feature: %s", feature_name)
            LOGGER.warning("Attempted to get feature_flag %s, but client wasn't initialized!", feature_name)
            return default_value
