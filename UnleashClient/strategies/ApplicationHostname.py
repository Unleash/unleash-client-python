# pylint: disable=invalid-name
import platform

from UnleashClient.strategies.Strategy import Strategy


class ApplicationHostname(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["hostNames"].split(",")]

    def apply(self, context: dict = None) -> bool:
        """
        Returns true if userId is a member of id list.

        :return:
        """
        return platform.node() in self.parsed_provisioning
