from fcache.cache import FileCache
from UnleashClient.api import get_feature_toggles
from UnleashClient.loader import load_features


def fetch_and_load_features(url: str,
                            app_name: str,
                            instance_id: str,
                            custom_headers: dict,
                            cache: FileCache,
                            strategies: dict) -> None:

    feature_provisioning = get_feature_toggles(url, app_name, instance_id, custom_headers)

    load_features(cache, feature_provisioning, strategies)
