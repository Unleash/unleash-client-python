import random
from UnleashClient.strategies import Strategy


class GradualRolloutRandom(Strategy):
    def __call__(self, context: dict = None) -> bool:
        """
        Returns random assignment.

        :return:
        """
        percentage = int(self.parameters["percentage"])

        return percentage > 0 and random.randint(1, 100) <= percentage
