from fcache.cache import FileCache
from UnleashClient.api import get_feature_toggles
from UnleashClient.loader import load_features
from UnleashClient.constants import FEATURES_URL, ETAG
from UnleashClient.utils import LOGGER


def fetch_and_load_features(url: str,
                            app_name: str,
                            instance_id: str,
                            custom_headers: dict,
                            custom_options: dict,
                            cache: FileCache,
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
        cache[ETAG]
    )

    if feature_provisioning:
        cache[FEATURES_URL] = feature_provisioning
        cache.sync()
    else:
        LOGGER.warning("Unable to get feature flag toggles, using cached provisioning.")

    if etag:
        cache[ETAG] = etag
        cache.sync()

    load_features(cache, features, strategy_mapping)
