import pytest
import uuid
from fcache.cache import FileCache
from UnleashClient.constants import FEATURES_URL
from tests.utilities.mocks import MOCK_ALL_FEATURES


@pytest.fixture()
def cache_empty():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    yield temporary_cache
    temporary_cache.delete()


@pytest.fixture()
def cache_full():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache[FEATURES_URL] = MOCK_ALL_FEATURES
    temporary_cache.sync()
    yield temporary_cache
    temporary_cache.delete()
