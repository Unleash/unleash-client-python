from UnleashClient.strategies.parameters import Parameter

# pylint: disable=dangerous-default-value
class StrategyV2:
    """
    In general, default & custom classes should only need to override:
    * __init__() - Depending on the parameters your feature needs
    * strategy() - Your feature provisioning
    """
    def __init__(self,
                 constraints: list = [],
                 parameters: Parameter = None,
                 ) -> None:
        """
        A generic strategy objects.

        :param constraints: List of 'constraints' objects derived from strategy section (...from feature section) of
        /api/clients/features response
        """
        self.parameters = parameters
        self.constraints = constraints

    def __call__(self, context: dict = None) -> bool:
        """
        Check constraints before applying strategy.

        :param context: Context information
        :return:
        """
        flag_state = False

        if all([constraint(context) for constraint in self.constraints]):
            flag_state = self.strategy(context)

        return flag_state

    def strategy(self, context: dict = None) -> bool:  #pylint: disable=W0613,R0201
        """
        Strategy implementation goes here.

        :param context:
        :return:
        """
        return False
