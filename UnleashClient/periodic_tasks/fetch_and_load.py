from UnleashClient.api import get_feature_toggles
from UnleashClient.loader import load_features
from UnleashClient.constants import FEATURES_URL, ETAG
from UnleashClient.utils import LOGGER
from UnleashClient.cache import BaseCache


def fetch_and_load_features(url: str,
                            app_name: str,
                            instance_id: str,
                            custom_headers: dict,
                            custom_options: dict,
                            cache: BaseCache,
                            features: dict,
                            strategy_mapping: dict,
                            project: str = None) -> None:
    (feature_provisioning, etag) = get_feature_toggles(
        url,
        app_name,
        instance_id,
        custom_headers,
        custom_options,
        project,
        cache.get(ETAG)
    )

    if feature_provisioning:
        cache.set(FEATURES_URL, feature_provisioning)
    else:
        LOGGER.warning("Unable to get feature flag toggles, using cached provisioning.")

    if etag:
        cache.set(ETAG, etag)

    load_features(cache, features, strategy_mapping)
