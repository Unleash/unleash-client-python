from UnleashClient.strategies import Strategy


class Default(Strategy):
    def __call__(self,
                 context: dict = None,
                 default_value: bool = False) -> bool:
        """
        Return true if enabled.

        :return:
        """
        return_value = default_value

        if self.enabled:
            return_value = True

        self.increment_stats(return_value)

        return return_value
