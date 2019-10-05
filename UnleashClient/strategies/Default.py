from UnleashClient.strategies import StrategyV2


class Default(StrategyV2):
    def apply_strategy(self, context: dict = None) -> bool:
        """
        Return true if enabled.

        :return:
        """
        return True
