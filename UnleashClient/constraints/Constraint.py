from UnleashClient.utils import LOGGER

class Constraint:
    def __init__(self, constraint_dict: dict) -> None:
        """
        Represents a constraint on a flexible rollout strategy

        constraint_dict = From the strategy document.
        """
        self.context_name = constraint_dict['contextName']
        self.operator = constraint_dict['operator']
        self.values = constraint_dict['values']

    def __call__(self, context: dict = None) -> bool:
        """
        Returns true/false depending on constraint provisioning and context.

        :param context: Context information
        :return:
        """
        constraint_check = False

        try:
            if self.context_name in context.keys():
                value = context[self.context_name]
            else:
                value = None
                constraint_check = False

            if value:
                if self.operator.upper() == "IN":
                    constraint_check = value in self.values
                elif self.operator.upper() == "NOT_IN":
                    constraint_check = value not in self.values
        except Exception as excep:  #pylint: disable=W0703
            LOGGER.info("Could not evaluate context %s!  Error: %s", self.context_name, excep)

        return constraint_check
