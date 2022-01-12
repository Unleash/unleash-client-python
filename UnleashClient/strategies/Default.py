# pylint: disable=invalid-name
from UnleashClient.strategies.Strategy import Strategy


class Default(Strategy):
    def apply(self, context: dict = None) -> bool:
        """
        Return true if enabled.

        :return:
        """
        return True
