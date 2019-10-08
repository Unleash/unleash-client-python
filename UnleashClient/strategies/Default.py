from UnleashClient.strategies.Strategies import Strategy


class Default(Strategy):
    def apply(self, context: dict = None) -> bool:
        """
        Return true if enabled.

        :return:
        """
        return True
