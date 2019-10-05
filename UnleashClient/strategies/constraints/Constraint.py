from UnleashClient.utils import LOGGER

class Constraint:
    def __init__(
            self,
            context_name: str,
            operator: str,
            values: list
    ) -> None:
        """
        Represents a constraint on a flexible rollout strategy

        :param context_name: Thing to constrain on
        :param operator: IN or NOT_IN
        :param values: List of values to compare against.
        """
        self.context_name = context_name
        self.operator = operator
        self.values = values

    def __call__(self, context: dict = None) -> bool:
        """
        Returns true/false depending on constraint provisioning and context.

        :param context: Context information
        :return:
        """
        constraint_check = False

        try:
            value = context[self.context_name]

            if self.operator.upper() == "IN":
                constraint_check = value in self.values
            elif self.operator.upper() == "NOT_IN":
                constraint_check = value not in self.values
        except Exception as excep:  #pylint: disable=W0703
            LOGGER.info("Could not evaluate context %s!  Error: %s", self.context_name, excep)

        return constraint_check
