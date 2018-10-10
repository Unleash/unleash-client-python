import random
from UnleashClient.strategies import Strategy


class GradualRolloutRandom(Strategy):
    def __call__(self, context: dict = None) -> bool:
        """
        Returns random assignment.

        :return:
        """
        percentage = self.parameters["percentage"]

        return percentage < random.randint(1, 100)
