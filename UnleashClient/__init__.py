"""
This is the core of the Python unleash client.
"""
from datetime import datetime
from fcache.cache import FileCache
from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from UnleashClient.api import register_client
from UnleashClient.periodic_tasks import fetch_and_load_features, aggregate_and_send_metrics
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
                 custom_headers: dict = {}) -> None:
        """
        Constructor for the unleash client class.

        :param url: URL of the unleash server, required.
        :param app_name: Name of the application using the unleash client, required.
        :param instance_id: Unique identifier for unleash client instance, optional & defaults to "unleash-client-python"
        :param refresh_interval: Provisioning refresh interval in ms, optional & defaults to 60000 ms (60 seconds)
        :param metrics_interval: Metrics refresh interval in ms, optional & defaults to 60000 ms (60 seconds)
        :param disable_metrics: Disables sending metrics to unleash server, optional & defaults to false.
        :param custom_headers: Default headers to send to unleash server, optional & defaults to empty.
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
        self.cache = FileCache("Unleash")
        self.features: dict = {}
        self.scheduler = BackgroundScheduler()
        self.fl_job: Job = None
        self.metric_job: Job = None
        self.metrics_last_sent_time = datetime.now()

        # Client status
        self.is_initialized = False

    def initialize_client(self) -> None:
        """
        Initializes client communication with central unleash server(s).

        This kicks off:
        * Provisioning poll
        * Stats poll

        :return:
        """
        # Setup
        fl_args = [self.unleash_url,
                   self.unleash_app_name,
                   self.unleash_instance_id,
                   self.unleash_custom_headers,
                   self.cache,
                   self.features]

        metrics_args = [self.unleash_url,
                        self.unleash_app_name,
                        self.unleash_instance_id,
                        self.unleash_custom_headers,
                        self.features,
                        self.metrics_last_sent_time]

        # Register app
        register_client(self.unleash_url, self.unleash_app_name, self.unleash_instance_id,
                        self.unleash_metrics_interval, self.unleash_custom_headers)

        fetch_and_load_features(*fl_args)

        # Start periodic jobs
        self.scheduler.start()
        self.fl_job = self.scheduler.add_job(fetch_and_load_features,
                                             trigger=IntervalTrigger(seconds=int(self.unleash_refresh_interval)),
                                             args=fl_args)

        self.metric_job = self.scheduler.add_job(aggregate_and_send_metrics,
                                                 trigger=IntervalTrigger(seconds=int(self.unleash_metrics_interval)),
                                                 args=metrics_args)

        self.is_initialized = True

    def destroy(self):
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
        """
        if self.is_initialized:
            try:
                return self.features[feature_name].is_enabled(context, default_value)
            except Exception as excep:
                LOGGER.warning("Error checking feature flag: %s", excep)
                return default_value
        else:
            LOGGER.warning("Attempted to get feature_flag %s, but client wasn't initialized!", feature_name)
            return default_value
