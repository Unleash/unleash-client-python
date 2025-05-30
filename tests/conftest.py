import typing
import uuid
from datetime import datetime, timezone
from sys import modules

import niquests
import pytest
import pytest_asyncio
import requests
from niquests.packages import urllib3

# the mock utility 'responses' need 'requests'
# but definitely works with 'niquests'.
modules["requests"] = niquests
modules["requests.adapters"] = niquests.adapters
modules["requests.exceptions"] = niquests.exceptions
modules["requests.compat"] = requests.compat
modules["requests.packages.urllib3"] = urllib3

# make 'responses' mock both sync and async
# 'Requests' ever only supported sync
# Fortunately interfaces are mirrored in 'Niquests'
from unittest import mock as std_mock  # noqa: E402

import responses  # noqa: E402


class NiquestsMock(responses.RequestsMock):
    """Asynchronous support for responses"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            target="niquests.adapters.HTTPAdapter.send",
            **kwargs,
        )

        self._patcher_async = None

    def unbound_on_async_send(self):
        async def send(
            adapter: "niquests.adapters.AsyncHTTPAdapter",
            request: "niquests.PreparedRequest",
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> "niquests.Response":
            if args:
                # that probably means that the request was sent from the custom adapter
                # It is fully legit to send positional args from adapter, although,
                # `requests` implementation does it always with kwargs
                # See for more info: https://github.com/getsentry/responses/issues/642
                try:
                    kwargs["stream"] = args[0]
                    kwargs["timeout"] = args[1]
                    kwargs["verify"] = args[2]
                    kwargs["cert"] = args[3]
                    kwargs["proxies"] = args[4]
                except IndexError:
                    # not all kwargs are required
                    pass

            resp = self._on_request(adapter, request, **kwargs)

            if kwargs["stream"]:
                return resp

            resp.__class__ = niquests.Response
            return resp

        return send

    def unbound_on_send(self):
        def send(
            adapter: "niquests.adapters.HTTPAdapter",
            request: "niquests.PreparedRequest",
            *args: typing.Any,
            **kwargs: typing.Any,
        ) -> "niquests.Response":
            if args:
                # that probably means that the request was sent from the custom adapter
                # It is fully legit to send positional args from adapter, although,
                # `requests` implementation does it always with kwargs
                # See for more info: https://github.com/getsentry/responses/issues/642
                try:
                    kwargs["stream"] = args[0]
                    kwargs["timeout"] = args[1]
                    kwargs["verify"] = args[2]
                    kwargs["cert"] = args[3]
                    kwargs["proxies"] = args[4]
                except IndexError:
                    # not all kwargs are required
                    pass

            return self._on_request(adapter, request, **kwargs)

        return send

    def start(self) -> None:
        if self._patcher:
            # we must not override value of the _patcher if already applied
            # this prevents issues when one decorated function is called from
            # another decorated function
            return

        self._patcher = std_mock.patch(target=self.target, new=self.unbound_on_send())
        self._patcher_async = std_mock.patch(
            target=self.target.replace("HTTPAdapter", "AsyncHTTPAdapter"),
            new=self.unbound_on_async_send(),
        )

        self._patcher.start()
        self._patcher_async.start()

    def stop(self, allow_assert: bool = True) -> None:
        if self._patcher:
            # prevent stopping unstarted patchers
            self._patcher.stop()
            self._patcher_async.stop()

            # once patcher is stopped, clean it. This is required to create a new
            # fresh patcher on self.start()
            self._patcher = None
            self._patcher_async = None

        if not self.assert_all_requests_are_fired:
            return

        if not allow_assert:
            return

        not_called = [m for m in self.registered() if m.call_count == 0]
        if not_called:
            raise AssertionError(
                "Not all requests have been executed {!r}".format(
                    [(match.method, match.url) for match in not_called]
                )
            )


mock = _default_mock = NiquestsMock(assert_all_requests_are_fired=False)

setattr(responses, "mock", mock)
setattr(responses, "_default_mock", _default_mock)

for kw in [
    "activate",
    "add",
    "_add_from_file",
    "add_callback",
    "add_passthru",
    "assert_call_count",
    "calls",
    "delete",
    "DELETE",
    "get",
    "GET",
    "head",
    "HEAD",
    "options",
    "OPTIONS",
    "patch",
    "PATCH",
    "post",
    "POST",
    "put",
    "PUT",
    "registered",
    "remove",
    "replace",
    "reset",
    "response_callback",
    "start",
    "stop",
    "upsert",
]:
    if not hasattr(responses, kw):
        continue
    setattr(responses, kw, getattr(mock, kw))

from tests.utilities.mocks import MOCK_ALL_FEATURES, MOCK_CUSTOM_STRATEGY  # noqa: E402
from tests.utilities.mocks.mock_features import (  # noqa: E402
    MOCK_FEATURES_WITH_SEGMENTS_RESPONSE,
)
from UnleashClient.asynchronous.cache import AsyncFileCache  # noqa: E402
from UnleashClient.cache import FileCache  # noqa: E402
from UnleashClient.constants import (  # noqa: E402
    ETAG,
    FEATURES_URL,
    METRIC_LAST_SENT_TIME,
)


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


@pytest_asyncio.fixture()
async def async_cache_empty():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = AsyncFileCache(cache_name)
    await temporary_cache.mset(
        {METRIC_LAST_SENT_TIME: datetime.now(timezone.utc), ETAG: ""}
    )
    yield temporary_cache
    temporary_cache.destroy()


@pytest_asyncio.fixture()
async def async_cache_full():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = AsyncFileCache(cache_name)
    await temporary_cache.mset(
        {
            FEATURES_URL: MOCK_ALL_FEATURES,
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: "",
        }
    )
    yield temporary_cache
    temporary_cache.destroy()


@pytest_asyncio.fixture()
async def async_cache_custom():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = AsyncFileCache(cache_name)
    await temporary_cache.mset(
        {
            FEATURES_URL: MOCK_CUSTOM_STRATEGY,
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: "",
        }
    )
    yield temporary_cache
    temporary_cache.destroy()


@pytest_asyncio.fixture()
async def async_cache_segments():
    cache_name = "pytest_%s" % uuid.uuid4()
    temporary_cache = AsyncFileCache(cache_name)
    await temporary_cache.mset(
        {
            FEATURES_URL: MOCK_FEATURES_WITH_SEGMENTS_RESPONSE,
            METRIC_LAST_SENT_TIME: datetime.now(timezone.utc),
            ETAG: "",
        }
    )
    yield temporary_cache
    temporary_cache.destroy()
