from UnleashClient.utils import LOGGER


# pylint: disable=dangerous-default-value, broad-except
class Feature:
    """
    Basic Strategy object
    """
    def __init__(self,
                 name: str,
                 enabled: bool,
                 strategies: list) -> None:
        """
        Base Strategy

        :param name:
        :param is_enabled:
        :param parameters: Parameters
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
        if result:
            self.yes_count += 1
        else:
            self.no_count += 1

    def is_enabled(self,
                   context: dict = None,
                   default_value: bool = False) -> bool:
        """
        Strategy implementation goes here.

        :param context: Context information
        :param default_value: Optional, but allows for override.
        :return:
        """
        flag_value = False

        try:
            for strategy in self.strategies:
                flag_value = flag_value or strategy(context)
        except Exception as strategy_except:
            LOGGER.warning("Error checking feature flag: %s", strategy_except)
            flag_value = default_value

        self.increment_stats(flag_value)

        return flag_value
