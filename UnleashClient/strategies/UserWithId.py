from UnleashClient.strategies.Strategies import StrategyV2


class UserWithId(StrategyV2):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["userIds"].split(',')]

    def apply_strategy(self, context: dict = None) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        return_value = False

        if "userId" in context.keys():
            return_value = context["userId"] in self.parsed_provisioning

        return return_value
