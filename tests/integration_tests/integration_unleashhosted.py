import logging
import sys
import time

from UnleashClient import UnleashClient
from UnleashClient.strategies import Strategy


# ---
class DogTest(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(",")]

    def apply(self, context: dict = None) -> bool:
        """
        Turn on if I'm a dog.

        :return:
        """
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value


# ---

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)
# ---

custom_strategies_dict = {
    "amIADog": DogTest,
}

my_client = UnleashClient(
    url="https://app.unleash-hosted.com/demo/api",
    environment="staging",
    app_name="pyIvan",
    custom_headers={
        "Authorization": "56907a2fa53c1d16101d509a10b78e36190b0f918d9f122d"
    },
    custom_strategies=custom_strategies_dict,
    verbose_log_level=10,
)

my_client.initialize_client()

while True:
    time.sleep(10)
    context = {"userId": "1", "sound": "woof"}
    print(f"ivantest: {my_client.is_enabled('ivantest', context)}")
    print(f"ivan-variations: {my_client.get_variant('ivan-variations', context)}")
    print(
        f"ivan-customstrategyx: {my_client.is_enabled('ivan-customstrategy', context)}"
    )
