from typing import Optional

from UnleashClient.api import get_feature_toggles
from UnleashClient.cache import BaseCache
from UnleashClient.constants import ETAG, FEATURES_URL
from UnleashClient.loader import load_features
from UnleashClient.utils import LOGGER


def fetch_and_load_features(
    url: str,
    app_name: str,
    instance_id: str,
    custom_headers: dict,
    custom_options: dict,
    cache: BaseCache,
    features: dict,
    strategy_mapping: dict,
    project: Optional[str] = None,
) -> None:
    (feature_provisioning, etag) = get_feature_toggles(
        url,
        app_name,
        instance_id,
        custom_headers,
        custom_options,
        project,
        cache.get(ETAG),
    )

    if feature_provisioning:
        cache.set(FEATURES_URL, feature_provisioning)
    else:
        LOGGER.debug(
            "No feature provisioning returned from server, using cached provisioning."
        )

    if etag:
        cache.set(ETAG, etag)

    load_features(cache, features, strategy_mapping)
