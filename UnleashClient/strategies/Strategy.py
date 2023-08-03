# pylint: disable=invalid-name,dangerous-default-value
import warnings
from dataclasses import dataclass
from typing import Iterator, Optional

from UnleashClient.constraints import Constraint
from UnleashClient.variants import Variants


@dataclass
class EvaluationResult:
    enabled: bool
    variant: Optional[dict]


class Strategy:
    """
    The parent class for default and custom strategies.

    In general, default & custom classes should only need to override:

    - ``__init__()`` - Depending on the parameters your feature needs
    - ``apply()`` - Your feature provisioning

    :param constraints: List of 'constraints' objects derived from strategy section (...from feature section) of `/api/clients/features` Unleash server response.
    :param variants: List of 'variant' objects derived from strategy section (...from feature section) of `/api/clients/features` Unleash server response.
    :param parameters: The 'parameter' objects from the strategy section (...from feature section) of `/api/clients/features` Unleash server response.
    """

    def __init__(
        self,
        constraints: list = [],
        parameters: dict = {},
        segment_ids: list = None,
        global_segments: dict = None,
        variants: list = None,
    ) -> None:
        self.parameters = parameters
        self.constraints = constraints
        self.variants = variants or []
        self.segment_ids = segment_ids or []
        self.global_segments = global_segments or {}
        self.parsed_provisioning = self.load_provisioning()

    def __call__(self, context: dict = None):
        warnings.warn(
            "unleash-client-python v3.x.x requires overriding the execute() method instead of the __call__() method.",
            DeprecationWarning,
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

    def get_result(self, context) -> EvaluationResult:
        enabled = self.execute(context)
        variant = None
        if enabled:
            variant = self.parsed_variants.get_variant(context, enabled)

        result = EvaluationResult(enabled, variant)
        return result

    @property
    def parsed_constraints(self) -> Iterator[Constraint]:
        for constraint_dict in self.constraints:
            yield Constraint(constraint_dict=constraint_dict)

        for segment_id in self.segment_ids:
            segment = self.global_segments[segment_id]
            for constraint in segment["constraints"]:
                yield Constraint(constraint_dict=constraint)

    @property
    def parsed_variants(self) -> Variants:
        return Variants(
            variants_list=self.variants,
            group_id=self.parameters.get("groupId"),
            is_feature_variants=False,
        )

    def load_provisioning(self) -> list:  # pylint: disable=no-self-use
        """
        Loads strategy provisioning from Unleash feature flag configuration.

        This should parse the raw values in ``self.parameters`` into format Python can comprehend.
        """
        return []

    def apply(
        self, context: dict = None
    ) -> bool:  # pylint: disable=unused-argument,no-self-use
        """
        Strategy implementation.

        :param context: Feature flag context
        :return: Feature flag result
        """
        return False
