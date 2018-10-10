from UnleashClient.strategies import Strategy


class UserWithId(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["userIds"].split(',')]

    def __call__(self, context: dict = None) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        return context["userId"] in self.parsed_provisioning
