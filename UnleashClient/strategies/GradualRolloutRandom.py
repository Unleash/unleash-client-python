import random
from UnleashClient.strategies.Strategies import StrategyV2


class GradualRolloutRandom(StrategyV2):
    def apply_strategy(self, context: dict = None) -> bool:
        """
        Returns random assignment.

        :return:
        """
        percentage = int(self.parameters["percentage"])

        return percentage > 0 and random.randint(1, 100) <= percentage
