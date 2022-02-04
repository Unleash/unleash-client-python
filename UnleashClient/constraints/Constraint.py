# pylint: disable=invalid-name, too-few-public-methods
from UnleashClient.utils import LOGGER, get_identifier


class Constraint:
    def __init__(self, constraint_dict: dict) -> None:
        """
        Represents a constraint on a strategy

        :param constraint_dict: From the strategy document.
        """
        self.context_name: str = constraint_dict['contextName']
        self.operator: str = constraint_dict['operator']
        self.values = constraint_dict['values'] if 'values' in constraint_dict.keys() else []
        self.value = constraint_dict['value'] if 'value' in constraint_dict.keys() else []

        self.case_insensitive = constraint_dict['caseInsensitive'] if 'caseInsensitive' in constraint_dict.keys() else False
        self.inverted = constraint_dict['inverted'] if 'inverted' in constraint_dict.keys() else False


    def apply(self, context: dict = None) -> bool:
        """
        Returns true/false depending on constraint provisioning and context.

        :param context: Context information
        :return:
        """
        constraint_check = False

        try:
            value = get_identifier(self.context_name, context)

            if value:
                if self.operator.upper() == "IN":
                    constraint_check = value in self.values
                elif self.operator.upper() == "NOT_IN":
                    constraint_check = value not in self.values
        except Exception as excep:  # pylint: disable=broad-except
            LOGGER.info("Could not evaluate context %s!  Error: %s", self.context_name, excep)

        return constraint_check
