# pylint: disable=invalid-name
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
        percentage = int(self.parameters["rollout"])
        activation_group = self.parameters["groupId"]
        stickiness = (
            self.parameters["stickiness"]
            if "stickiness" in self.parameters
            else "default"
        )

        if stickiness == "default":
            if "userId" in context.keys():
                calculated_percentage = normalized_hash(
                    context["userId"], activation_group
                )
            elif "sessionId" in context.keys():
                calculated_percentage = normalized_hash(
                    context["sessionId"], activation_group
                )
            else:
                calculated_percentage = self.random_hash()
        elif stickiness == "random":
            calculated_percentage = self.random_hash()
        else:
            custom_stickiness = (
                context.get(stickiness) or context.get("properties")[stickiness]
            )
            calculated_percentage = normalized_hash(custom_stickiness, activation_group)

        return percentage > 0 and calculated_percentage <= percentage
