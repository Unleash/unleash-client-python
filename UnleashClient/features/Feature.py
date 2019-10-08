import warnings
from UnleashClient.utils import LOGGER
from UnleashClient.strategies import Strategy


# pylint: disable=dangerous-default-value, broad-except
class Feature:
    def __init__(self,
                 name: str,
                 enabled: bool,
                 strategies: list) -> None:
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
        self.__deprecation_check()

        flag_value = default_value

        if self.enabled:
            try:
                strategy_result = any([x.execute(context) for x in self.strategies])
                flag_value = flag_value or strategy_result
            except Exception as strategy_except:
                LOGGER.warning("Error checking feature flag: %s", strategy_except)

        self.increment_stats(flag_value)

        LOGGER.info("Feature toggle status for feature %s: %s", self.name, flag_value)

        return flag_value

    def __deprecation_check(self):
        """
        Notify users of backwards incompatible changes in v3 for custom strategies.
        """
        for strategy in self.strategies:
            try:
                # Check if the __call__() method is overwritten (should only be true for custom strategies in v1.x or v2.x.
                if strategy.__call__ != Strategy.__call__:
                    warnings.warn(
                        "unleash-client-python v3.x.x requires overriding the execute() method instead of the __call__() method. Error in: {}".format(type(strategy)),
                        DeprecationWarning
                    )
            except AttributeError:
                # Ignore if not.
                pass
