# pylint: disable=invalid-name
from UnleashClient.strategies.Strategy import Strategy


class UserWithId(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["userIds"].split(",")]

    def apply(self, context: dict = None) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        return_value = False

        if "userId" in context.keys():
            return_value = context["userId"] in self.parsed_provisioning

        return return_value
