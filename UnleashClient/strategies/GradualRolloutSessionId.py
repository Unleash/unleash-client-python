# pylint: disable=invalid-name
from UnleashClient.strategies.Strategy import Strategy
from UnleashClient.utils import normalized_hash


class GradualRolloutSessionId(Strategy):
    def apply(self, context: dict = None) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        percentage = int(self.parameters["percentage"])
        activation_group = self.parameters["groupId"]

        return (
            percentage > 0
            and normalized_hash(context["sessionId"], activation_group) <= percentage
        )
