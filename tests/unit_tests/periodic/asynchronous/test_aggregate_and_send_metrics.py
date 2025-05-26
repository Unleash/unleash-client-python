import json

import pytest
import responses
from yggdrasil_engine.engine import UnleashEngine

from tests.utilities.testing_constants import (
    APP_NAME,
    CONNECTION_ID,
    CUSTOM_HEADERS,
    CUSTOM_OPTIONS,
    INSTANCE_ID,
    REQUEST_TIMEOUT,
    URL,
)
from UnleashClient.constants import (
    CLIENT_SPEC_VERSION,
    METRICS_URL,
)
from UnleashClient.periodic_tasks.asynchronous import async_aggregate_and_send_metrics

FULL_METRICS_URL = URL + METRICS_URL
print(FULL_METRICS_URL)


@pytest.mark.asyncio
@responses.activate
async def test_no_metrics():
    responses.add(responses.POST, FULL_METRICS_URL, json={}, status=200)

    engine = UnleashEngine()

    await async_aggregate_and_send_metrics(
        URL,
        APP_NAME,
        INSTANCE_ID,
        CONNECTION_ID,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
        REQUEST_TIMEOUT,
        engine,
    )

    assert len(responses.calls) == 0


@pytest.mark.asyncio
@responses.activate
async def test_metrics_metadata_is_sent():
    responses.add(responses.POST, FULL_METRICS_URL, json={}, status=200)

    engine = UnleashEngine()
    engine.count_toggle("something-to-make-sure-metrics-get-sent", True)

    await async_aggregate_and_send_metrics(
        URL,
        APP_NAME,
        INSTANCE_ID,
        CONNECTION_ID,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
        REQUEST_TIMEOUT,
        engine,
    )

    assert len(responses.calls) == 1
    request = json.loads(responses.calls[0].request.body)

    assert request["yggdrasilVersion"] is not None
    assert request["specVersion"] == CLIENT_SPEC_VERSION
    assert request["platformName"] is not None
    assert request["platformVersion"] is not None
