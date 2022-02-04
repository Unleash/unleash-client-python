# pylint: disable=invalid-name, too-few-public-methods, use-a-generator
from enum import Enum
from UnleashClient.utils import LOGGER, get_identifier


class ConstraintOperators(Enum):
    IN = "IN"
    NOT_IN = "NOT_IN"
    STR_ENDS_WITH = "STR_ENDS_WITH"
    STR_STARTS_WITH = "STR_STARTS_WITH"
    STR_CONTAINS = "STR_CONTAINS"

class Constraint:
    def __init__(self, constraint_dict: dict) -> None:
        """
        Represents a constraint on a strategy

        :param constraint_dict: From the strategy document.
        """
        self.context_name: str = constraint_dict['contextName']
        self.operator: ConstraintOperators = ConstraintOperators(constraint_dict['operator'].upper())
        self.values = constraint_dict['values'] if 'values' in constraint_dict.keys() else []
        self.value = constraint_dict['value'] if 'value' in constraint_dict.keys() else []

        self.case_insensitive = constraint_dict['caseInsensitive'] if 'caseInsensitive' in constraint_dict.keys() else False
        self.inverted = constraint_dict['inverted'] if 'inverted' in constraint_dict.keys() else False


    # Methods to handle each operator type.
    def check_list_operators(self, context_value: str) -> bool:
        return_value = False

        if self.operator == ConstraintOperators.IN:
            return_value = context_value in self.values
        elif self.operator == ConstraintOperators.NOT_IN:
            return_value = context_value not in self.values

        return return_value

    def check_string_operators(self, context_value: str) -> bool:
        if self.case_insensitive:
            normalized_values = [x.upper() for x in self.values]
            normalized_context_value = context_value.upper()
        else:
            normalized_values = self.values
            normalized_context_value = context_value

        return_value = False

        if self.operator == ConstraintOperators.STR_CONTAINS:
            return_value = any([x in normalized_context_value for x in normalized_values])
        elif self.operator == ConstraintOperators.STR_ENDS_WITH:
            return_value = any([normalized_context_value.endswith(x) for x in normalized_values])
        elif self.operator == ConstraintOperators.STR_STARTS_WITH:
            return_value = any([normalized_context_value.startswith(x) for x in normalized_values])

        return return_value

    def apply(self, context: dict = None) -> bool:
        """
        Returns true/false depending on constraint provisioning and context.

        :param context: Context information
        :return:
        """
        constraint_check = False

        try:
            context_value = get_identifier(self.context_name, context)

            if context_value:
                if self.operator in [ConstraintOperators.IN, ConstraintOperators.NOT_IN]:
                    constraint_check = self.check_list_operators(context_value=context_value)
                if self.operator in [ConstraintOperators.STR_CONTAINS, ConstraintOperators.STR_ENDS_WITH, ConstraintOperators.STR_STARTS_WITH]:
                    constraint_check = self.check_string_operators(context_value=context_value)
        except Exception as excep:  # pylint: disable=broad-except
            LOGGER.info("Could not evaluate context %s!  Error: %s", self.context_name, excep)

        return not constraint_check if self.inverted else constraint_check
