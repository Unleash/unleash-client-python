import responses

from tests.utilities.mocks import MOCK_CUSTOM_STRATEGY
from tests.utilities.old_code.StrategyV2 import StrategyOldV2
from tests.utilities.testing_constants import APP_NAME, URL
from UnleashClient import UnleashClient
from UnleashClient.constants import FEATURES_URL, METRICS_URL, REGISTER_URL
from UnleashClient.strategies import Strategy


class CatTest(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(",")]

    def apply(self, context: dict = None) -> bool:
        """
        Turn on if I'm a cat.

        :return:
        """
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value


class DogTest(StrategyOldV2):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(",")]

    def _call_(self, context: dict = None) -> bool:
        """
        Turn on if I'm a dog.

        :return:
        """
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value


@responses.activate
def test_uc_customstrategy_happypath(recwarn):
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_CUSTOM_STRATEGY, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {"amIACat": CatTest, "amIADog": DogTest}

    unleash_client = UnleashClient(
        URL, APP_NAME, environment="prod", custom_strategies=custom_strategies_dict
    )

    unleash_client.initialize_client()

    # Check custom strategy.
    assert unleash_client.is_enabled("CustomToggle", {"sound": "meow"})
    assert not unleash_client.is_enabled("CustomToggle", {"sound": "bark"})

    # Check warning on deprecated strategy.
    assert len(recwarn) >= 1
    assert any([x.category == DeprecationWarning for x in recwarn])


@responses.activate
def test_uc_customstrategy_depredationwarning():
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_CUSTOM_STRATEGY, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {"amIACat": CatTest, "amIADog": DogTest}

    unleash_client = UnleashClient(
        URL, APP_NAME, environment="prod", custom_strategies=custom_strategies_dict
    )

    unleash_client.initialize_client()

    # Check a toggle that contains an outdated custom strategy
    assert unleash_client.is_enabled("CustomToggleWarning", {"sound": "meow"})


@responses.activate
def test_uc_customstrategy_safemulti():
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_CUSTOM_STRATEGY, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {"amIACat": CatTest, "amIADog": DogTest}

    unleash_client = UnleashClient(
        URL, APP_NAME, environment="prod", custom_strategies=custom_strategies_dict
    )

    unleash_client.initialize_client()

    # Check a toggle that contains an outdated custom strategy and a default strategy.
    assert unleash_client.is_enabled("CustomToggleWarningMultiStrat", {"sound": "meow"})
