# pylint: disable=invalid-name
from typing import Dict, Optional, cast

from UnleashClient.constants import DISABLED_VARIATION
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

    def is_enabled(
        self, context: dict = None, default_value: bool = False
    ) -> bool:  # pylint: disable=unused-argument
        """
        Checks if feature is enabled.

        :param context: Context information
        :param default_value: Deprecated!  Users should use the fallback_function on the main is_enabled() method.
        :return:
        """
        flag_value = False

        if self.enabled:
            try:
                if self.strategies:
                    strategy_result = any(x.execute(context) for x in self.strategies)
                else:
                    # If no strategies are present, should default to true. This isn't possible via UI.
                    strategy_result = True

                flag_value = strategy_result
            except Exception as strategy_except:
                LOGGER.warning("Error checking feature flag: %s", strategy_except)

        self.increment_stats(flag_value)

        LOGGER.info("Feature toggle status for feature %s: %s", self.name, flag_value)

        return flag_value

    def get_variant(self, context: dict = None) -> dict:
        """
        Checks if feature is enabled and, if so, get the variant.

        :param context: Context information
        :return:
        """
        variant = DISABLED_VARIATION
        is_feature_enabled = self.is_enabled(context)

        if is_feature_enabled and self.variants is not None:
            try:
                variant = self.variants.get_variant(context)
                variant["enabled"] = is_feature_enabled
            except Exception as variant_exception:
                LOGGER.warning("Error selecting variant: %s", variant_exception)

        self._count_variant(cast(str, variant["name"]))
        return variant

    @staticmethod
    def metrics_only_feature(feature_name: str):
        feature = Feature(feature_name, False, [])
        feature.only_for_metrics = True
        return feature
