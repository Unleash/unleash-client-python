# pylint: disable=invalid-name, too-few-public-methods
from typing import List
from enum import Enum
from UnleashClient.utils import LOGGER, get_identifier


class ConstraintOperators(Enum):
    IN = "IN"
    NOT_IN = "NOT_IN"


class Constraint:
    def __init__(self, constraint_dict: dict) -> None:
        """
        Represents a constraint on a strategy

        :param constraint_dict: From the strategy document.
        """
        self.context_name: str = constraint_dict['contextName']
        self.operator: str = ConstraintOperators(constraint_dict['operator'].upper())
        self.values = constraint_dict['values'] if 'values' in constraint_dict.keys() else []
        self.value = constraint_dict['value'] if 'value' in constraint_dict.keys() else []

        self.case_insensitive = constraint_dict['caseInsensitive'] if 'caseInsensitive' in constraint_dict.keys() else False
        self.inverted = constraint_dict['inverted'] if 'inverted' in constraint_dict.keys() else False


    @staticmethod
    def check_in(context_value: str, values: List[str]) -> bool:
        return context_value in values


    @staticmethod
    def check_not_in(context_value: str, values: List[str]) -> bool:
        return context_value not in values


    def check_list_operators(self, context_value: str) -> bool:
        if self.operator == ConstraintOperators.IN:
            return self.check_in(context_value, self.values)
        elif self.operator == ConstraintOperators.NOT_IN:
            return self.check_not_in(context_value, self.values)
        else:
            return False


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
        except Exception as excep:  # pylint: disable=broad-except
            LOGGER.info("Could not evaluate context %s!  Error: %s", self.context_name, excep)

        return constraint_check
