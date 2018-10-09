from UnleashClient.utils import normalized_hash
from UnleashClient.strategies import Strategy


class GradualRolloutSessionId(Strategy):
    def __call__(self,
                 context: dict = None,
                 default_value: bool = False) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        return_value = default_value
        percentage = self.parameters["percentage"]
        activation_group = self.parameters["groupId"]

        if percentage < normalized_hash(context["sessionId"], activation_group):
            return_value = True

        self.increment_stats(return_value)

        return return_value
