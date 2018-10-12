# pylint: disable=dangerous-default-value
class Strategy():
    """
    In general, default & custom classes should only need to override:
    * __call__() - Implementation of the strategy.
    * load_provisioning - Loads strategy provisioning
    """
    def __init__(self,
                 parameters: dict = {}) -> None:
        """
        A generic strategy objects.

        :param parameters: 'parameters' key from strategy section (...from feature section) of
        /api/clients/features response
        """
        # Experiment information
        self.parameters = parameters

        self.parsed_provisioning = self.load_provisioning()

    # pylint: disable=no-self-use
    def load_provisioning(self) -> list:
        """
        Method to load data on object initialization, if desired.

        This should parse the raw values in self.parameters into format Python can comprehend.
        """
        return []

    def __eq__(self, other):
        return self.parameters == other.parameters

    def __call__(self, context: dict = None) -> bool:
        """
        Strategy implementation goes here.

        :param context: Context information
        :return:
        """
        return False
