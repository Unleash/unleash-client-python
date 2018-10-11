import pytest
import responses
from fcache.cache import FileCache
from tests.utilities.mocks.mock_features import MOCK_FEATURE_RESPONSE
from tests.utilities.testing_constants import URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS
from UnleashClient.constants import FEATURES_URL
from UnleashClient.periodic_tasks import fetch_and_load_features
from UnleashClient.features import Feature


FULL_FEATURE_URL = URL + FEATURES_URL


@pytest.fixture()
def temp_cache():
    temporary_cache = FileCache('pytest')
    yield temporary_cache
    temporary_cache.delete()


@responses.activate
def test_fetch_and_load(temp_cache):
    in_memory_features = {}
    responses.add(responses.GET, FULL_FEATURE_URL, json=MOCK_FEATURE_RESPONSE, status=200)

    fetch_and_load_features(URL,
                            APP_NAME,
                            INSTANCE_ID,
                            CUSTOM_HEADERS,
                            temp_cache,
                            in_memory_features)

    assert isinstance(in_memory_features["testFlag"], Feature)
