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
        A representation of a feature object

        :param name: Name of the feature.
        :param enabled: Whether feature is enabled.
        :param strategies: List of sub-classed Strategy objects representing feature strategies.
        """
        # Experiment information
        self.name = name
        self.enabled = enabled
        self.strategies = strategies
        self.variants = variants

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
                   default_value: bool = False) -> bool:  # pylint: disable=unused-argument
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

    def get_variant(self,
                    context: dict = None) -> dict:
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
                variant['enabled'] = is_feature_enabled
            except Exception as variant_exception:
                LOGGER.warning("Error selecting variant: %s", variant_exception)

        return variant
