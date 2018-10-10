# pylint: disable=dangerous-default-value
class Strategy():
    """
    Basic Strategy object
    """
    def __init__(self,
                 parameters: dict = {}) -> None:
        """
        Base strategy object

        :param name:
        :param is_enabled:
        :param parameters: Parameters
        """
        # Experiment information
        self.parameters = parameters

        self.parsed_provisioning = self.load_provisioning()

    # pylint: disable=no-self-use
    def load_provisioning(self) -> list:
        """
        Method to load data on object initialization, if desired.
        """
        return []

    def __eq__(self, other):
        return self.parameters == other.parameters

    def __call__(self, context: dict = None) -> bool:
        """
        Strategy implementation goes here.

        :param context: Context information
        :param default_value: Optional, but allows for override.
        :return:
        """
        return False
