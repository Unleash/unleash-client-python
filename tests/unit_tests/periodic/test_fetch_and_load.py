import responses
from UnleashClient.constants import FEATURES_URL
from UnleashClient.periodic_tasks import fetch_and_load_features
from UnleashClient.features import Feature
from tests.utilities.mocks.mock_features import MOCK_FEATURE_RESPONSE
from tests.utilities.testing_constants import URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS, DEFAULT_STRATEGY_MAPPING
from tests.utilities.decorators import cache_empty  # noqa: F401


FULL_FEATURE_URL = URL + FEATURES_URL


@responses.activate  # noqa: F811
def test_fetch_and_load(cache_empty):
    # Set up for tests
    in_memory_features = {}
    responses.add(responses.GET, FULL_FEATURE_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    temp_cache = cache_empty

    fetch_and_load_features(URL,
                            APP_NAME,
                            INSTANCE_ID,
                            CUSTOM_HEADERS,
                            temp_cache,
                            in_memory_features,
                            DEFAULT_STRATEGY_MAPPING)

    assert isinstance(in_memory_features["testFlag"], Feature)


@responses.activate  # noqa: F811
def test_fetch_and_load_failure(cache_empty):
    # Set up for tests
    in_memory_features = {}
    responses.add(responses.GET, FULL_FEATURE_URL, json=MOCK_FEATURE_RESPONSE, status=200)
    temp_cache = cache_empty

    fetch_and_load_features(URL,
                            APP_NAME,
                            INSTANCE_ID,
                            CUSTOM_HEADERS,
                            temp_cache,
                            in_memory_features,
                            DEFAULT_STRATEGY_MAPPING)

    # Fail next request
    responses.reset()
    responses.add(responses.GET, FULL_FEATURE_URL, json={}, status=500)

    fetch_and_load_features(URL,
                            APP_NAME,
                            INSTANCE_ID,
                            CUSTOM_HEADERS,
                            temp_cache,
                            in_memory_features,
                            DEFAULT_STRATEGY_MAPPING)

    assert isinstance(in_memory_features["testFlag"], Feature)
