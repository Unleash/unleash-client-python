from UnleashClient.strategies import Strategy


class UserWithId(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["userIds"].split(',')]

    def __call__(self,
                 context: dict = None,
                 default_value: bool = False) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        return_value = default_value

        if context["userId"] in self.parsed_provisioning:
            return_value = True

        self.increment_stats(return_value)

        return return_value
