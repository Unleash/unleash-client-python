from fcache.cache import FileCache
from UnleashClient.features import Feature
from UnleashClient.constants import FEATURES_URL
from UnleashClient.utils import LOGGER

# pylint: disable=broad-except
def _create_strategies(provisioning: dict,
                       strategy_mapping: dict) -> list:
    feature_strategies = []

    for strategy in provisioning["strategies"]:
        try:
            if "parameters" in strategy.keys():
                feature_strategies.append(strategy_mapping[strategy["name"]](strategy["parameters"]))
            else:
                feature_strategies.append(strategy_mapping[strategy["name"]])  # type: ignore
        except Exception as excep:
            LOGGER.warning("Failed to load strategy.  This may be a problem with a custom strategy.  Exception: %s",
                           excep)

    return feature_strategies


def _create_feature(provisioning: dict,
                    strategy_mapping: dict) -> Feature:
    if "strategies" in provisioning.keys():
        parsed_strategies = _create_strategies(provisioning, strategy_mapping)
    else:
        parsed_strategies = []

    return Feature(name=provisioning["name"],
                   enabled=provisioning["enabled"],
                   strategies=parsed_strategies)


def load_features(cache: FileCache,
                  feature_toggles: dict,
                  strategy_mapping: dict) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param feature_toggles: Should be the features class variable from UnleashClient
    :return:
    """
    # Pull raw provisioning from cache.
    feature_provisioning = cache[FEATURES_URL]

    # Parse provisioning
    parsed_features = {}
    feature_names = [d["name"] for d in feature_provisioning["features"]]

    for provisioning in feature_provisioning["features"]:
        parsed_features[provisioning["name"]] = provisioning

    # Delete old features/cache
    for feature in list(feature_toggles.keys()):
        if feature not in feature_names:
            del feature_toggles[feature]

    # Update existing objects
    for feature in feature_toggles.keys():
        feature_for_update = feature_toggles[feature]
        strategies = parsed_features[feature]["strategies"]

        feature_for_update.enabled = parsed_features[feature]["enabled"]
        if strategies:
            parsed_strategies = _create_strategies(parsed_features[feature], strategy_mapping)
            feature_for_update.strategies = parsed_strategies

    # Handle creation or deletions
    new_features = list(set(feature_names) - set(feature_toggles.keys()))

    for feature in new_features:
        feature_toggles[feature] = _create_feature(parsed_features[feature], strategy_mapping)
