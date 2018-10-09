import random
from UnleashClient.strategies import Strategy


class GradualRolloutRandom(Strategy):
    def __call__(self,
                 context: dict = None,
                 default_value: bool = False) -> bool:
        """
        Returns random assignment.

        :return:
        """
        return_value = default_value
        percentage = self.parameters["percentage"]

        if percentage < random.randint(1, 100):
            return_value = True

        self.increment_stats(return_value)

        return return_value
