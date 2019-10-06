import responses
from UnleashClient import UnleashClient
from UnleashClient.strategies import Strategy, StrategyV2
from tests.utilities.testing_constants import URL, APP_NAME
from tests.utilities.mocks import MOCK_CUSTOM_STRATEGY
from UnleashClient.constants import REGISTER_URL, FEATURES_URL, METRICS_URL


class CatTest(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(',')]

    def __call__(self, context: dict = None) -> bool:
        """
        Turn on if I'm a cat.

        :return:
        """
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value


class DogTest(StrategyV2):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(',')]

    def apply_strategy(self, context: dict = None) -> bool:
        """
        Turn on if I'm a dog.

        :return:
        """
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value


@responses.activate
def test_uc_custom_strategy():
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_CUSTOM_STRATEGY, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {
        "amIACat": CatTest
    }

    unleash_client = UnleashClient(URL, APP_NAME, custom_strategies=custom_strategies_dict)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()

    assert unleash_client.is_enabled("CustomToggle", {"sound": "meow"})
    assert not unleash_client.is_enabled("CustomToggle", {"sound": "bark"})


@responses.activate
def test_uc_custom_strategyv2():
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_CUSTOM_STRATEGY, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {
        "amIADog": DogTest
    }

    unleash_client = UnleashClient(URL, APP_NAME, environment="staging", custom_strategies=custom_strategies_dict)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()

    assert not unleash_client.is_enabled("CustomToggleV2", {"sound": "meow"})
    assert unleash_client.is_enabled("CustomToggleV2", {"sound": "bark"})
