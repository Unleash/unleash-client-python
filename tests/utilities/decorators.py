import pytest
import uuid
from datetime import datetime, timezone
from fcache.cache import FileCache
from UnleashClient.constants import FEATURES_URL, METRIC_LAST_SENT_TIME, ETAG
from tests.utilities.mocks import MOCK_ALL_FEATURES, MOCK_CUSTOM_STRATEGY


@pytest.fixture()
def cache_empty():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache[METRIC_LAST_SENT_TIME] = datetime.now(timezone.utc)
    temporary_cache[ETAG] = ''
    yield temporary_cache
    temporary_cache.delete()


@pytest.fixture()
def cache_full():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache[FEATURES_URL] = MOCK_ALL_FEATURES
    temporary_cache[METRIC_LAST_SENT_TIME] = datetime.now(timezone.utc)
    temporary_cache[ETAG] = ''
    temporary_cache.sync()
    yield temporary_cache
    temporary_cache.delete()


@pytest.fixture()
def cache_custom():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache[FEATURES_URL] = MOCK_CUSTOM_STRATEGY
    temporary_cache[METRIC_LAST_SENT_TIME] = datetime.now(timezone.utc)
    temporary_cache[ETAG] = ''
    temporary_cache.sync()
    yield temporary_cache
    temporary_cache.delete()
