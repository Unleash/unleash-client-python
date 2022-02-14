import pytest
import uuid
from datetime import datetime, timezone
from UnleashClient.constants import FEATURES_URL, METRIC_LAST_SENT_TIME, ETAG
from tests.utilities.mocks import MOCK_ALL_FEATURES, MOCK_CUSTOM_STRATEGY
from UnleashClient.cache import FileCache


@pytest.fixture()
def cache_empty():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset({
        METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
        ETAG: ''
    })
    yield temporary_cache
    temporary_cache.destroy()


@pytest.fixture()
def cache_full():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset({
        FEATURES_URL: MOCK_ALL_FEATURES,
        METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
        ETAG: ''
    })
    yield temporary_cache
    temporary_cache.destroy()


@pytest.fixture()
def cache_custom():
    cache_name = 'pytest_%s' % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset({
        FEATURES_URL: MOCK_CUSTOM_STRATEGY,
        METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
        ETAG: ''
    })
    yield temporary_cache
    temporary_cache.destroy()
