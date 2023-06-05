import json
from datetime import datetime, timedelta, timezone

import responses

from tests.utilities.mocks.mock_variants import VARIANTS
from tests.utilities.testing_constants import (
    APP_NAME,
    CUSTOM_HEADERS,
    CUSTOM_OPTIONS,
    INSTANCE_ID,
    IP_LIST,
    URL,
)
from UnleashClient.cache import FileCache
from UnleashClient.constants import METRIC_LAST_SENT_TIME, METRICS_URL
from UnleashClient.features import Feature
from UnleashClient.periodic_tasks import aggregate_and_send_metrics
from UnleashClient.strategies import Default, RemoteAddress
from UnleashClient.variants import Variants

FULL_METRICS_URL = URL + METRICS_URL
print(FULL_METRICS_URL)


@responses.activate
def test_aggregate_and_send_metrics():
    responses.add(responses.POST, FULL_METRICS_URL, json={}, status=200)

    start_time = datetime.now(timezone.utc) - timedelta(seconds=60)
    cache = FileCache("TestCache")
    cache.set(METRIC_LAST_SENT_TIME, start_time)
    strategies = [RemoteAddress(parameters={"IPs": IP_LIST}), Default()]
    my_feature1 = Feature("My Feature1", True, strategies)
    my_feature1.yes_count = 1
    my_feature1.no_count = 1

    my_feature2 = Feature(
        "My Feature2", True, strategies, variants=Variants(VARIANTS, "My Feature2")
    )
    my_feature2.yes_count = 2
    my_feature2.no_count = 2

    feature2_variant_counts = {
        "VarA": 56,
        "VarB": 0,
        "VarC": 4,
    }
    my_feature2.variant_counts = feature2_variant_counts

    my_feature3 = Feature("My Feature3", True, strategies)
    my_feature3.yes_count = 0
    my_feature3.no_count = 0

    features = {"My Feature1": my_feature1, "My Feature 2": my_feature2}

    aggregate_and_send_metrics(
        URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS, CUSTOM_OPTIONS, features, cache
    )

    assert len(responses.calls) == 1
    request = json.loads(responses.calls[0].request.body)

    assert len(request["bucket"]["toggles"].keys()) == 2
    assert request["bucket"]["toggles"]["My Feature1"]["yes"] == 1
    assert request["bucket"]["toggles"]["My Feature1"]["no"] == 1
    assert (
        request["bucket"]["toggles"]["My Feature2"]["variants"]
        == feature2_variant_counts
    )
    assert "My Feature3" not in request["bucket"]["toggles"].keys()
    assert cache.get(METRIC_LAST_SENT_TIME) > start_time


@responses.activate
def test_no_metrics():
    responses.add(responses.POST, FULL_METRICS_URL, json={}, status=200)

    start_time = datetime.now(timezone.utc) - timedelta(seconds=60)
    cache = FileCache("TestCache")
    cache.set(METRIC_LAST_SENT_TIME, start_time)
    strategies = [RemoteAddress(parameters={"IPs": IP_LIST}), Default()]

    my_feature1 = Feature("My Feature1", True, strategies)
    my_feature1.yes_count = 0
    my_feature1.no_count = 0

    features = {"My Feature1": my_feature1}

    aggregate_and_send_metrics(
        URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS, CUSTOM_OPTIONS, features, cache
    )

    assert len(responses.calls) == 0
