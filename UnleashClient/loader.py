from fcache.cache import FileCache
from UnleashClient.features import Feature
from UnleashClient.strategies import ApplicationHostname, Default, GradualRolloutRandom, \
    GradualRolloutSessionId, GradualRolloutUserId, UserWithId, RemoteAddress

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
                  feature_provisioning: dict,
                  strategies: dict) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param feature_provisioning: JSON from /api/client/features
    :param strategies: Should be the features class variable from UnleashClient
    :return:
    """
    # Delete old features/cache
    for feature in cache.keys():
        if feature not in [d["name"] for d in feature_provisioning["features"]]:
            del strategies[feature]
            del cache[feature]

    # Parse feature_provisioning and load into cache / update to cache
    for feature in feature_provisioning["features"]:
        if feature["name"] not in cache.keys():
            cache[feature["name"]] = feature
        else:
            if cache[feature["name"]] != feature:
                cache[feature["name"]] = feature

        cache.sync()

    # Update existing objects
    for feature in strategies.keys():
        feature_for_update = strategies[feature]

        feature_for_update.enabled = cache[feature]["enabled"]
        feature_for_update.strategies = _create_strategies(cache[feature]["strategies"])

    # Handle creation or deletions
    new_features = list(set(cache.keys()) - set(strategies.keys()))

    for feature in new_features:
        strategies[feature] = _create_feature(cache[feature])
