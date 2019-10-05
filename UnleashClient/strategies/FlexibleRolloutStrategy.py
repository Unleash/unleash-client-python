import random
from UnleashClient.strategies.Strategy_v2 import StrategyV2
from UnleashClient.utils import normalized_hash


class FlexibleRollout(StrategyV2):
    @staticmethod
    def random_hash() -> int:
        return random.randint(1, 100)

    def __call__(self, context: dict = None) -> bool:
        """
        If constraints are satisfied, return a percentage rollout on provisioned.

        :return:
        """
        strategy_value = False

        if all([constraint(context) for constraint in self.constraints]):
            percentage = int(self.parameters["rollout"])
            activation_group = self.parameters["groupId"]

            if self.parameters['stickiness'].lower() == 'default':
                if 'userId' in context.keys():
                    calculated_percentage = normalized_hash(context['userId'], activation_group)
                elif 'sessionId' in context.keys():
                    calculated_percentage = normalized_hash(context['sessionId'], activation_group)
                else:
                    calculated_percentage = self.random_hash()
            elif self.parameters['stickiness'] in ['userId', 'sessionId']:
                calculated_percentage = normalized_hash(context[self.parameters["stickiness"]], activation_group)
            else:
                # This technically handles the stickiness == random scenario.
                calculated_percentage = self.random_hash()

            strategy_value = percentage > 0 and calculated_percentage <= percentage

        return strategy_value
