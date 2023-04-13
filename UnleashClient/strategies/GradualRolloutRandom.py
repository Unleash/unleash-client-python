# pylint: disable=invalid-name
import random

from UnleashClient.strategies.Strategy import Strategy


class GradualRolloutRandom(Strategy):
    def apply(self, context: dict = None) -> bool:
        """
        Returns random assignment.

        :return:
        """
        percentage = int(self.parameters["percentage"])

        return percentage > 0 and random.randint(1, 100) <= percentage
