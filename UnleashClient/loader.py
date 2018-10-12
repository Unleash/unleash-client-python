from fcache.cache import FileCache
from UnleashClient.features import Feature
from UnleashClient.strategies import ApplicationHostname, Default, GradualRolloutRandom, \
    GradualRolloutSessionId, GradualRolloutUserId, UserWithId, RemoteAddress
from UnleashClient.constants import FEATURES_URL

STRATEGY_TO_OBJECT = {
    "applicationHostname": ApplicationHostname,
    "default": Default,
    "gradualRolloutRandom": GradualRolloutRandom,
    "gradualRolloutSessionId": GradualRolloutSessionId,
    "gradualRolloutUserId": GradualRolloutUserId,
    "remoteAddress": RemoteAddress,
    "userWithId": UserWithId
}


def _create_strategies(provisioning: dict) -> list:
    feature_strategies = []

    for strategy in provisioning:
        feature_strategies.append(STRATEGY_TO_OBJECT[strategy["name"]](strategy["parameters"]))

    return feature_strategies


def _create_feature(provisioning: dict) -> Feature:
    return Feature(name=provisioning["name"],
                   enabled=provisioning["enabled"],
                   strategies=_create_strategies(provisioning["strategies"]))


def load_features(cache: FileCache,
                  strategies: dict) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param strategies: Should be the features class variable from UnleashClient
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
    for feature in list(strategies.keys()):
        if feature not in feature_names:
            del strategies[feature]

    # Update existing objects
    for feature in list(strategies.keys()):
        feature_for_update = strategies[feature]

        feature_for_update.enabled = parsed_features[feature]["enabled"]
        feature_for_update.strategies = _create_strategies(parsed_features[feature]["strategies"])

    # Handle creation or deletions
    new_features = list(set(feature_names) - set(strategies.keys()))

    for feature in new_features:
        strategies[feature] = _create_feature(parsed_features[feature])
