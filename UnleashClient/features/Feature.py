# pylint: disable=invalid-name
from typing import Dict, Optional, cast

from UnleashClient.constants import DISABLED_VARIATION
from UnleashClient.strategies import EvaluationResult, Strategy
from UnleashClient.utils import LOGGER
from UnleashClient.variants import Variants


# pylint: disable=dangerous-default-value, broad-except
class Feature:
    def __init__(
        self,
        name: str,
        enabled: bool,
        strategies: list,
        variants: Optional[Variants] = None,
        impression_data: bool = False,
        dependencies: list = None,
    ) -> None:
        """
        A representation of a feature object

        :param name: Name of the feature.
        :param enabled: Whether feature is enabled.
        :param strategies: List of sub-classed Strategy objects representing feature strategies.
        :param impression_data: Whether impression data is enabled.
        """
        # Experiment information
        self.name = name
        self.enabled = enabled
        self.strategies = strategies
        self.variants = variants

        # Additional information
        self.impression_data = impression_data

        # Stats tracking
        self.yes_count = 0
        self.no_count = 0
        ## { [ variant name ]: number }
        self.variant_counts: Dict[str, int] = {}

        # Whether the feature exists only for tracking metrics or not.
        self.only_for_metrics = False

        # Prerequisite state of other features that this feature depends on
        self.dependencies = [
            dict(dependency, enabled=dependency.get("enabled", True))
            for dependency in dependencies or []
        ]

    def reset_stats(self) -> None:
        """
        Resets stats after metrics reporting

        :return:
        """
        self.yes_count = 0
        self.no_count = 0
        self.variant_counts = {}

    def increment_stats(self, result: bool) -> None:
        """
        Increments stats.

        :param result:
        :return:
        """
        if result:
            self.yes_count += 1
        else:
            self.no_count += 1

    def _count_variant(self, variant_name: str) -> None:
        """
        Count a specific variant.

        :param variant_name: The name of the variant to count.
        :return:
        """
        self.variant_counts[variant_name] = self.variant_counts.get(variant_name, 0) + 1

    def is_enabled(self, context: dict = None, skip_stats: bool = False) -> bool:
        """
        Checks if feature is enabled.

        :param context: Context information
        :return:
        """
        evaluation_result = self._get_evaluation_result(context, skip_stats)

        flag_value = evaluation_result.enabled

        return flag_value

    def get_variant(self, context: dict = None, skip_stats: bool = False) -> dict:
        """
        Checks if feature is enabled and, if so, get the variant.

        :param context: Context information
        :return:
        """
        evaluation_result = self._get_evaluation_result(context)
        is_feature_enabled = evaluation_result.enabled
        variant = evaluation_result.variant
        if variant is None or (is_feature_enabled and variant == DISABLED_VARIATION):
            try:
                LOGGER.debug("Getting variant from feature: %s", self.name)
                variant = (
                    self.variants.get_variant(context, is_feature_enabled)
                    if is_feature_enabled
                    else DISABLED_VARIATION
                )

            except Exception as variant_exception:
                LOGGER.warning("Error selecting variant: %s", variant_exception)
        if not skip_stats:
            self._count_variant(cast(str, variant["name"]))

        return {**variant, "feature_enabled": is_feature_enabled}

    def _get_evaluation_result(
        self, context: dict = None, skip_stats: bool = False
    ) -> EvaluationResult:
        strategy_result = EvaluationResult(False, None)
        if self.enabled:
            try:
                if self.strategies:
                    enabled_strategy: Strategy = next(
                        (x for x in self.strategies if x.execute(context)), None
                    )
                    if enabled_strategy is not None:
                        strategy_result = enabled_strategy.get_result(context)

                else:
                    # If no strategies are present, should default to true. This isn't possible via UI.
                    strategy_result = EvaluationResult(True, None)

            except Exception as evaluation_except:
                LOGGER.warning("Error getting evaluation result: %s", evaluation_except)

        if not skip_stats:
            self.increment_stats(strategy_result.enabled)
        LOGGER.info("%s evaluation result: %s", self.name, strategy_result)
        return strategy_result

    @staticmethod
    def metrics_only_feature(feature_name: str):
        feature = Feature(feature_name, False, [])
        feature.only_for_metrics = True
        return feature
