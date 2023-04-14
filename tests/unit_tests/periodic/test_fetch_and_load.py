import responses

from tests.utilities.mocks.mock_features import (
    MOCK_FEATURE_RESPONSE,
    MOCK_FEATURE_RESPONSE_PROJECT,
)
from tests.utilities.testing_constants import (
    APP_NAME,
    CUSTOM_HEADERS,
    CUSTOM_OPTIONS,
    DEFAULT_STRATEGY_MAPPING,
    ETAG_VALUE,
    INSTANCE_ID,
    PROJECT_NAME,
    PROJECT_URL,
    URL,
)
from UnleashClient.constants import ETAG, FEATURES_URL
from UnleashClient.features import Feature
from UnleashClient.periodic_tasks import fetch_and_load_features

FULL_FEATURE_URL = URL + FEATURES_URL


@responses.activate
def test_fetch_and_load(cache_empty):  # noqa: F811
    # Set up for tests
    in_memory_features = {}
    responses.add(
        responses.GET,
        FULL_FEATURE_URL,
        json=MOCK_FEATURE_RESPONSE,
        status=200,
        headers={"etag": ETAG_VALUE},
    )
    temp_cache = cache_empty

    fetch_and_load_features(
        URL,
        APP_NAME,
        INSTANCE_ID,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
        temp_cache,
        in_memory_features,
        DEFAULT_STRATEGY_MAPPING,
    )

    assert isinstance(in_memory_features["testFlag"], Feature)
    assert temp_cache.get(ETAG) == ETAG_VALUE


@responses.activate
def test_fetch_and_load_project(cache_empty):  # noqa: F811
    # Set up for tests
    in_memory_features = {}
    responses.add(
        responses.GET, PROJECT_URL, json=MOCK_FEATURE_RESPONSE_PROJECT, status=200
    )
    temp_cache = cache_empty

    fetch_and_load_features(
        URL,
        APP_NAME,
        INSTANCE_ID,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
        temp_cache,
        in_memory_features,
        DEFAULT_STRATEGY_MAPPING,
        PROJECT_NAME,
    )

    assert len(in_memory_features.keys()) == 1
    assert isinstance(in_memory_features["ivan-project"], Feature)


@responses.activate
def test_fetch_and_load_failure(cache_empty):  # noqa: F811
    # Set up for tests
    in_memory_features = {}
    responses.add(
        responses.GET, FULL_FEATURE_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    temp_cache = cache_empty

    fetch_and_load_features(
        URL,
        APP_NAME,
        INSTANCE_ID,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
        temp_cache,
        in_memory_features,
        DEFAULT_STRATEGY_MAPPING,
    )

    # Fail next request
    responses.reset()
    responses.add(responses.GET, FULL_FEATURE_URL, json={}, status=500)

    fetch_and_load_features(
        URL,
        APP_NAME,
        INSTANCE_ID,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
        temp_cache,
        in_memory_features,
        DEFAULT_STRATEGY_MAPPING,
    )

    assert isinstance(in_memory_features["testFlag"], Feature)
