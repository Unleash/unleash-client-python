from UnleashClient.variants import Variants
from UnleashClient.utils import LOGGER
from UnleashClient.constants import DISABLED_VARIATION


# pylint: disable=dangerous-default-value, broad-except
class Feature:
    def __init__(self,
                 name: str,
                 enabled: bool,
                 strategies: list,
                 variants: Variants = None) -> None:
        """
        An representation of a fewature object

        :param name: Name of the feature.
        :param enabled: Whether feature is enabled.
        :param strategies: List of sub-classed Strategy objects representing feature strategies.
        """
        # Experiment information
        self.name = name
        self.enabled = enabled
        self.strategies = strategies
        self.variations = variants

        # Stats tracking
        self.yes_count = 0
        self.no_count = 0

    def reset_stats(self) -> None:
        """
        Resets stats after metrics reporting

        :return:
        """
        self.yes_count = 0
        self.no_count = 0

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

    def is_enabled(self,
                   context: dict = None,
                   default_value: bool = False) -> bool:
        """
        Checks if feature is enabled.

        :param context: Context information
        :param default_value: Optional, but allows for override.
        :return:
        """
        flag_value = default_value

        if self.enabled:
            try:
                if self.strategies:
                    strategy_result = any([x.execute(context) for x in self.strategies])
                else:
                    # If no strategies are present, should default to true.  This isn't possible via UI.
                    strategy_result = True

                flag_value = flag_value or strategy_result
            except Exception as strategy_except:
                LOGGER.warning("Error checking feature flag: %s", strategy_except)

        self.increment_stats(flag_value)

        LOGGER.info("Feature toggle status for feature %s: %s", self.name, flag_value)

        return flag_value

    def get_variant(self,
                    context: dict = None) -> dict:
        """
        Checks if feature is enabled and, if so, get the variant.

        :param context: Context information
        :return:
        """
        is_feature_enabled = self.is_enabled(context)

        if is_feature_enabled and self.variations is not None:
            try:
                variant = self.variations.get_variant(context)
                variant['enabled'] = is_feature_enabled
            except Exception as variant_exception:
                LOGGER.warning("Error selecting variant: %s", variant_exception)
        else:
            variant = DISABLED_VARIATION

        return variant
