import uuid
from datetime import datetime, timezone

import pytest

from tests.utilities.mocks import MOCK_ALL_FEATURES, MOCK_CUSTOM_STRATEGY
from tests.utilities.mocks.mock_features import MOCK_FEATURES_WITH_SEGMENTS_RESPONSE
from UnleashClient.cache import FileCache
from UnleashClient.constants import ETAG, FEATURES_URL, METRIC_LAST_SENT_TIME


@pytest.fixture()
def cache_empty():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset({METRIC_LAST_SENT_TIME: datetime.now(timezone.utc), ETAG: ""})
    yield temporary_cache
    temporary_cache.destroy()


@pytest.fixture()
def cache_full():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset(
        {
            FEATURES_URL: MOCK_ALL_FEATURES,
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: "",
        }
    )
    yield temporary_cache
    temporary_cache.destroy()


@pytest.fixture()
def cache_custom():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset(
        {
            FEATURES_URL: MOCK_CUSTOM_STRATEGY,
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: "",
        }
    )
    yield temporary_cache
    temporary_cache.destroy()


@pytest.fixture()
def cache_segments():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = FileCache(cache_name)
    temporary_cache.mset(
        {
            FEATURES_URL: MOCK_FEATURES_WITH_SEGMENTS_RESPONSE,
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: "",
        }
    )
    yield temporary_cache
    temporary_cache.destroy()
