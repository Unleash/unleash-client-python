from UnleashClient.constraints import Constraint

# pylint: disable=dangerous-default-value
class StrategyV2:
    """
    In general, default & custom classes should only need to override:
    * __init__() - Depending on the parameters your feature needs
    * strategy() - Your feature provisioning
    """
    def __init__(self,
                 constraints: list = [],
                 parameters: dict = {},
                 ) -> None:
        """
        A generic strategy objects.

        :param constraints: List of 'constraints' objects derived from strategy section (...from feature section) of
        /api/clients/features response
        :param parameters: The 'parameter' objects from the strategy section (...from feature section) of
        /api/clients/features response
        """
        self.parameters = parameters
        self.parsed_constraints = self.load_constraints(constraints)

    def __call__(self, context: dict = None) -> bool:
        """
        Check constraints before applying strategy.

        :param context: Context information
        :return:
        """
        flag_state = False

        if all([constraint(context) for constraint in self.parsed_constraints]):
            flag_state = self.strategy(context)

        return flag_state

    def load_constraints(self, constraints_list: list) -> list:  #pylint: disable=R0201
        """
        Loads constraints from provisioning.

        :return:
        """
        parsed_constraints_list = []

        for constraint_dict in constraints_list:
            parsed_constraints_list.append(Constraint(constraint_dict=constraint_dict))

        return parsed_constraints_list

    # pylint: disable=no-self-use
    def load_provisioning(self) -> list:
        """
        Method to load data on object initialization, if desired.

        This should parse the raw values in self.parameters into format Python can comprehend.
        """
        return []

    def strategy(self, context: dict = None) -> bool:  #pylint: disable=W0613,R0201
        """
        Strategy implementation goes here.

        :param context:
        :return:
        """
        return False
