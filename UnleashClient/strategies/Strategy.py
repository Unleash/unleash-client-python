# pylint: disable=dangerous-default-value
class Strategy():
    """
    Basic Strategy object
    """
    def __init__(self,
                 name: str,
                 enabled: bool,
                 parameters: dict = {}) -> None:
        """
        Base strategy object

        :param name:
        :param is_enabled:
        :param parameters: Parameters
        """
        # Experiment information
        self.name = name
        self.enabled = enabled
        self.parameters = parameters

        # Stats tracking
        self.yes_count = 0
        self.no_count = 0

        self.parsed_provisioning = self.load_provisioning()

    # pylint: disable=no-self-use
    def load_provisioning(self) -> list:
        """
        Method to load data on object initialization, if desired.
        """
        return []

    def reset_stats(self) -> None:
        """
        Resets stats after metrics reporting

        :return:
        """
        self.yes_count = 0
        self.no_count = 0

    def increment_stats(self, result: bool) -> None:
        if result:
            self.yes_count += 1
        else:
            self.no_count += 1

    def __call__(self,
                 context: dict = None,
                 default_value: bool = False) -> bool:
        """
        Strategy implementation goes here.

        :param context: Context information
        :param default_value: Optional, but allows for override.
        :return:
        """
        return False
