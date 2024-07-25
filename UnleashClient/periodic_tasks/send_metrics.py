from collections import ChainMap
from datetime import datetime, timezone
from platform import python_implementation, python_version

from UnleashClient.api import send_metrics
from UnleashClient.cache import BaseCache
from UnleashClient.constants import CLIENT_SPEC_VERSION, METRIC_LAST_SENT_TIME
from UnleashClient.utils import LOGGER


def aggregate_metrics(
    features: dict,
) -> dict:
    feature_stats_list = []

    for feature_name in features.keys():
        if not (features[feature_name].yes_count or features[feature_name].no_count):
            continue

        feature_stats = {
            features[feature_name].name: {
                "yes": features[feature_name].yes_count,
                "no": features[feature_name].no_count,
                "variants": features[feature_name].variant_counts,
            }
        }

        feature_stats_list.append(feature_stats)

    return dict(ChainMap(*feature_stats_list))


def aggregate_and_send_metrics(
    url: str,
    app_name: str,
    instance_id: str,
    custom_headers: dict,
    custom_options: dict,
    features: dict,
    cache: BaseCache,
    request_timeout: int,
) -> None:
    feature_stats_dict = aggregate_metrics(features)

    for feature_name in features.keys():
        features[feature_name].reset_stats()

    metrics_request = {
        "appName": app_name,
        "instanceId": instance_id,
        "bucket": {
            "start": cache.get(METRIC_LAST_SENT_TIME).isoformat(),
            "stop": datetime.now(timezone.utc).isoformat(),
            "toggles": feature_stats_dict,
        },
        "platformName": python_implementation(),
        "platformVersion": python_version(),
        "yggdrasilVersion": None,
        "specVersion": CLIENT_SPEC_VERSION,
    }

    if feature_stats_dict:
        send_metrics(
            url, metrics_request, custom_headers, custom_options, request_timeout
        )
        cache.set(METRIC_LAST_SENT_TIME, datetime.now(timezone.utc))
    else:
        LOGGER.debug("No feature flags with metrics, skipping metrics submission.")
