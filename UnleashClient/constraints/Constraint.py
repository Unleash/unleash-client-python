# pylint: disable=invalid-name, too-few-public-methods, use-a-generator
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Union

try:
    from semver import VersionInfo
except ImportError:
    # https://python-semver.readthedocs.io/en/latest/migration/migratetosemver3.html
    from semver.version import Version as VersionInfo

from dateutil.parser import parse

from UnleashClient.utils import LOGGER, get_identifier


class ConstraintOperators(Enum):
    # Logical operators
    IN = "IN"
    NOT_IN = "NOT_IN"

    # String operators
    STR_ENDS_WITH = "STR_ENDS_WITH"
    STR_STARTS_WITH = "STR_STARTS_WITH"
    STR_CONTAINS = "STR_CONTAINS"

    # Numeric oeprators
    NUM_EQ = "NUM_EQ"
    NUM_GT = "NUM_GT"
    NUM_GTE = "NUM_GTE"
    NUM_LT = "NUM_LT"
    NUM_LTE = "NUM_LTE"

    # Date operators
    DATE_AFTER = "DATE_AFTER"
    DATE_BEFORE = "DATE_BEFORE"

    # Semver operators
    SEMVER_EQ = "SEMVER_EQ"
    SEMVER_GT = "SEMVER_GT"
    SEMVER_LT = "SEMVER_LT"


class Constraint:
    def __init__(self, constraint_dict: dict) -> None:
        """
        Represents a constraint on a strategy

        :param constraint_dict: From the strategy document.
        """
        self.context_name: str = constraint_dict["contextName"]
        self.operator: ConstraintOperators = ConstraintOperators(
            constraint_dict["operator"].upper()
        )
        self.values = (
            constraint_dict["values"] if "values" in constraint_dict.keys() else []
        )
        self.value = (
            constraint_dict["value"] if "value" in constraint_dict.keys() else None
        )

        self.case_insensitive = (
            constraint_dict["caseInsensitive"]
            if "caseInsensitive" in constraint_dict.keys()
            else False
        )
        self.inverted = (
            constraint_dict["inverted"]
            if "inverted" in constraint_dict.keys()
            else False
        )

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
            return_value = any(
                [x in normalized_context_value for x in normalized_values]
            )
        elif self.operator == ConstraintOperators.STR_ENDS_WITH:
            return_value = any(
                [normalized_context_value.endswith(x) for x in normalized_values]
            )
        elif self.operator == ConstraintOperators.STR_STARTS_WITH:
            return_value = any(
                [normalized_context_value.startswith(x) for x in normalized_values]
            )

        return return_value

    def check_numeric_operators(self, context_value: Union[float, int]) -> bool:
        return_value = False

        parsed_value = float(self.value)
        parsed_context = float(context_value)

        if self.operator == ConstraintOperators.NUM_EQ:
            return_value = parsed_context == parsed_value
        elif self.operator == ConstraintOperators.NUM_GT:
            return_value = parsed_context > parsed_value
        elif self.operator == ConstraintOperators.NUM_GTE:
            return_value = parsed_context >= parsed_value
        elif self.operator == ConstraintOperators.NUM_LT:
            return_value = parsed_context < parsed_value
        elif self.operator == ConstraintOperators.NUM_LTE:
            return_value = parsed_context <= parsed_value
        return return_value

    def check_date_operators(self, context_value: Union[datetime, str]) -> bool:
        return_value = False
        parsing_exception = False

        DateUtilParserError: Any

        try:
            from dateutil.parser import ParserError

            DateUtilParserError = ParserError
        except ImportError:
            DateUtilParserError = ValueError

        try:
            parsed_date = parse(self.value)
            if isinstance(context_value, str):
                context_date = parse(context_value)
            else:
                context_date = context_value
        except DateUtilParserError:
            LOGGER.error(f"Unable to parse date: {self.value}")
            parsing_exception = True

        if not parsing_exception:
            if self.operator == ConstraintOperators.DATE_AFTER:
                return_value = context_date > parsed_date
            elif self.operator == ConstraintOperators.DATE_BEFORE:
                return_value = context_date < parsed_date

        return return_value

    def check_semver_operators(self, context_value: str) -> bool:
        return_value = False
        parsing_exception = False
        target_version: Optional[VersionInfo] = None
        context_version: Optional[VersionInfo] = None

        try:
            target_version = VersionInfo.parse(self.value)
        except ValueError:
            LOGGER.error(f"Unable to parse server semver: {self.value}")
            parsing_exception = True

        try:
            context_version = VersionInfo.parse(context_value)
        except ValueError:
            LOGGER.error(f"Unable to parse context semver: {context_value}")
            parsing_exception = True

        if not parsing_exception:
            if self.operator == ConstraintOperators.SEMVER_EQ:
                return_value = context_version == target_version
            elif self.operator == ConstraintOperators.SEMVER_GT:
                return_value = context_version > target_version
            elif self.operator == ConstraintOperators.SEMVER_LT:
                return_value = context_version < target_version

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

            # Set currentTime if not specified
            if self.context_name == "currentTime" and not context_value:
                context_value = datetime.now()

            if context_value is not None:
                if self.operator in [
                    ConstraintOperators.IN,
                    ConstraintOperators.NOT_IN,
                ]:
                    constraint_check = self.check_list_operators(
                        context_value=context_value
                    )
                elif self.operator in [
                    ConstraintOperators.STR_CONTAINS,
                    ConstraintOperators.STR_ENDS_WITH,
                    ConstraintOperators.STR_STARTS_WITH,
                ]:
                    constraint_check = self.check_string_operators(
                        context_value=context_value
                    )
                elif self.operator in [
                    ConstraintOperators.NUM_EQ,
                    ConstraintOperators.NUM_GT,
                    ConstraintOperators.NUM_GTE,
                    ConstraintOperators.NUM_LT,
                    ConstraintOperators.NUM_LTE,
                ]:
                    constraint_check = self.check_numeric_operators(
                        context_value=context_value
                    )
                elif self.operator in [
                    ConstraintOperators.DATE_AFTER,
                    ConstraintOperators.DATE_BEFORE,
                ]:
                    constraint_check = self.check_date_operators(
                        context_value=context_value
                    )
                elif self.operator in [
                    ConstraintOperators.SEMVER_EQ,
                    ConstraintOperators.SEMVER_GT,
                    ConstraintOperators.SEMVER_LT,
                ]:
                    constraint_check = self.check_semver_operators(
                        context_value=context_value
                    )
            # This is a special case in the client spec - so it's getting it's own handler here
            elif self.operator is ConstraintOperators.NOT_IN:  # noqa: PLR5501
                constraint_check = True

        except Exception as excep:  # pylint: disable=broad-except
            LOGGER.info(
                "Could not evaluate context %s!  Error: %s", self.context_name, excep
            )

        return not constraint_check if self.inverted else constraint_check
