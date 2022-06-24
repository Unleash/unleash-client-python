# pylint: disable=invalid-name,dangerous-default-value
from typing import Iterator
import warnings
from UnleashClient.constraints import Constraint


class Strategy:
    """
    The parent class for default and custom strategies.

    In general, default & custom classes should only need to override:

    - ``__init__()`` - Depending on the parameters your feature needs
    - ``apply()`` - Your feature provisioning

    :param constraints: List of 'constraints' objects derived from strategy section (...from feature section) of `/api/clients/features` Unleash server response.
    :param parameters: The 'parameter' objects from the strategy section (...from feature section) of `/api/clients/features` Unleash server response.
    """

    def __init__(self,
                 constraints: list = [],
                 parameters: dict = {},
                 segment_ids: list = None,
                 global_segments: dict = None
                 ) -> None:
        self.parameters = parameters
        self.constraints = constraints
        self.segment_ids = segment_ids or []
        self.global_segments = global_segments or {}
        self.parsed_provisioning = self.load_provisioning()

    def __call__(self, context: dict = None):
        warnings.warn(
            "unleash-client-python v3.x.x requires overriding the execute() method instead of the __call__() method.",
            DeprecationWarning
        )

    def execute(self, context: dict = None) -> bool:
        """
        Executes the strategies by:

        - Checking constraints
        - Applying the strategy

        This is what UnleashClient calls when you run ``is_enabled()``

        :param context: Feature flag context.
        :return: Feature flag result.
        """
        flag_state = False

        if all(constraint.apply(context) for constraint in self.parsed_constraints):
            flag_state = self.apply(context)

        return flag_state

    @property
    def parsed_constraints(self) -> Iterator[Constraint]:
        for constraint_dict in self.constraints:
            yield Constraint(constraint_dict=constraint_dict)

        for segment_id in self.segment_ids:
            segment = self.global_segments[segment_id]
            for constraint in segment["constraints"]:
                yield Constraint(constraint_dict=constraint)

    def load_provisioning(self) -> list:  # pylint: disable=no-self-use
        """
        Loads strategy provisioning from Unleash feature flag configuration.

        This should parse the raw values in ``self.parameters`` into format Python can comprehend.
        """
        return []

    def apply(self, context: dict = None) -> bool:  # pylint: disable=unused-argument,no-self-use
        """
        Strategy implementation.

        :param context: Feature flag context
        :return: Feature flag result
        """
        return False
