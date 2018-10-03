"""
This is the core of the Python unleash client.
"""
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
                 refresh_interval: int = 15000,
                 metrics_interval: int = 60000,
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
        self.unleash_url = url
        self.unleash_app_name = app_name
        self.unleash_instance_id = instance_id
        self.unleash_refresh_interval = refresh_interval
        self.unleash_metrics_interval = metrics_interval
        self.unleash_disable_metrics = disable_metrics
        self.unleash_custom_headers = custom_headers

        # Client status
        self.is_initialized = False

        self.logger = LOGGER

    def initialize_client(self) -> None:
        """
        Initializes client communication with central unleash server(s).

        This kicks off:
        * Provisioning poll
        * Stats poll

        :return:
        """
        # Register app

        # Start refresh polling

        # Start metrics polling

    def is_enabled(self) -> bool:
        """
        """
        return False
