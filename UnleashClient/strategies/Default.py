from UnleashClient.strategies import Strategy


class Default(Strategy):
    def __call__(self, context: dict = None) -> bool:
        """
        Return true if enabled.

        :return:
        """
        return True
