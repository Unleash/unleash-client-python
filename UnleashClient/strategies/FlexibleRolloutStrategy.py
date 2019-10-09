import random
from UnleashClient.strategies.Strategy import Strategy
from UnleashClient.utils import normalized_hash


class FlexibleRollout(Strategy):
    @staticmethod
    def random_hash() -> int:
        return random.randint(1, 100)

    def apply(self, context: dict = None) -> bool:
        """
        If constraints are satisfied, return a percentage rollout on provisioned.

        :return:
        """
        percentage = int(self.parameters['rollout'])
        activation_group = self.parameters['groupId']
        stickiness = self.parameters['stickiness']

        if stickiness == 'default':
            if 'userId' in context.keys():
                calculated_percentage = normalized_hash(context['userId'], activation_group)
            elif 'sessionId' in context.keys():
                calculated_percentage = normalized_hash(context['sessionId'], activation_group)
            else:
                calculated_percentage = self.random_hash()
        elif stickiness in ['userId', 'sessionId']:
            calculated_percentage = normalized_hash(context[stickiness], activation_group)
        else:
            # This also handles the stickiness == random scenario.
            calculated_percentage = self.random_hash()

        return percentage > 0 and calculated_percentage <= percentage
