import time
import json
import pytest
import responses
from UnleashClient import UnleashClient
from UnleashClient.strategies import Strategy
from tests.utilities.testing_constants import URL, ENVIRONMENT, APP_NAME, INSTANCE_ID, REFRESH_INTERVAL, \
    METRICS_INTERVAL, DISABLE_METRICS, DISABLE_REGISTRATION, CUSTOM_HEADERS
from tests.utilities.mocks.mock_features import MOCK_FEATURE_RESPONSE
from tests.utilities.mocks.mock_all_features import MOCK_ALL_FEATURES
from UnleashClient.constants import REGISTER_URL, FEATURES_URL, METRICS_URL


class EnvironmentStrategy(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["environments"].split(',')]

    def __call__(self, context: dict = None) -> bool:
        """
        Turn on if environemnt is a match.

        :return:
        """
        default_value = False

        if "environment" in context.keys():
            default_value = context["environment"] in self.parsed_provisioning

        return default_value


@pytest.fixture()
def unleash_client():
    unleash_client = UnleashClient(URL, APP_NAME, refresh_interval=REFRESH_INTERVAL, metrics_interval=METRICS_INTERVAL)
    yield unleash_client
    unleash_client.destroy()


@pytest.fixture()
def unleash_client_toggle_only():
    unleash_client = UnleashClient(URL,
                                   APP_NAME,
                                   refresh_interval=REFRESH_INTERVAL,
                                   metrics_interval=METRICS_INTERVAL,
                                   disable_registration=True,
                                   disable_metrics=True)
    yield unleash_client
    unleash_client.destroy()


def test_UC_initialize_default():
    client = UnleashClient(URL, APP_NAME)
    assert client.unleash_url == URL
    assert client.unleash_app_name == APP_NAME
    assert client.unleash_metrics_interval == 60


def test_UC_initialize_full():
    client = UnleashClient(URL,
                           APP_NAME,
                           ENVIRONMENT,
                           INSTANCE_ID,
                           REFRESH_INTERVAL,
                           METRICS_INTERVAL,
                           DISABLE_METRICS,
                           DISABLE_REGISTRATION,
                           CUSTOM_HEADERS)
    assert client.unleash_instance_id == INSTANCE_ID
    assert client.unleash_refresh_interval == REFRESH_INTERVAL
    assert client.unleash_metrics_interval == METRICS_INTERVAL
    assert client.unleash_disable_metrics == DISABLE_METRICS
    assert client.unleash_disable_registration == DISABLE_REGISTRATION
    assert client.unleash_custom_headers == CUSTOM_HEADERS


def test_UC_type_violation():
    client = UnleashClient(URL, APP_NAME, refresh_interval="60")
    assert client.unleash_url == URL
    assert client.unleash_app_name == APP_NAME
    assert client.unleash_refresh_interval == "60"


@responses.activate
def test_uc_lifecycle(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_initialized
    assert len(unleash_client.features) == 3

    # Simulate server provisioning change
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_ALL_FEATURES, status=200)
    time.sleep(30)
    assert len(unleash_client.features) == 7


@responses.activate
def test_uc_is_enabled(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_enabled("testFlag")


@responses.activate
def test_uc_is_enabled_with_context():
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {
        "custom-context": EnvironmentStrategy
    }

    unleash_client = UnleashClient(URL, APP_NAME, environment='prod', custom_strategies=custom_strategies_dict)
    # Create Unleash client and check initial load
    unleash_client.initialize_client()

    time.sleep(1)
    assert unleash_client.is_enabled("testContextFlag")
    unleash_client.destroy()


@responses.activate
def test_uc_is_enabled_error_states(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert not unleash_client.is_enabled("ThisFlagDoesn'tExist")
    assert unleash_client.is_enabled("ThisFlagDoesn'tExist", default_value=True)


@responses.activate
def test_uc_not_initialized():
    unleash_client = UnleashClient(URL, APP_NAME)
    assert not unleash_client.is_enabled("ThisFlagDoesn'tExist")
    assert unleash_client.is_enabled("ThisFlagDoesn'tExist", default_value=True)


@responses.activate
def test_uc_metrics(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_enabled("testFlag")

    time.sleep(12)
    request = json.loads(responses.calls[-1].request.body)
    assert request['bucket']["toggles"]["testFlag"]["yes"] == 1


@responses.activate
def test_uc_disabled_registration(unleash_client_toggle_only):
    unleash_client = unleash_client_toggle_only
    # Set up APIs
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=401)
    responses.add(responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=401)

    unleash_client.initialize_client()
    unleash_client.is_enabled("testFlag")
    time.sleep(20)
    assert unleash_client.is_enabled("testFlag")

    for api_call in responses.calls:
        assert '/api/client/features' in api_call.request.url
