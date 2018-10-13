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

    for strategy in provisioning["strategies"]:
        if "parameters" in strategy.keys():
            feature_strategies.append(STRATEGY_TO_OBJECT[strategy["name"]](strategy["parameters"]))
        else:
            feature_strategies.append(STRATEGY_TO_OBJECT[strategy["name"]])  # type: ignore

    return feature_strategies


def _create_feature(provisioning: dict) -> Feature:
    if "strategies" in provisioning.keys():
        parsed_strategies = _create_strategies(provisioning)
    else:
        parsed_strategies = []

    return Feature(name=provisioning["name"],
                   enabled=provisioning["enabled"],
                   strategies=parsed_strategies)


def load_features(cache: FileCache,
                  feature_toggles: dict) -> None:
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
            parsed_strategies = _create_strategies(parsed_features[feature])
            feature_for_update.strategies = parsed_strategies

    # Handle creation or deletions
    new_features = list(set(feature_names) - set(feature_toggles.keys()))

    for feature in new_features:
        feature_toggles[feature] = _create_feature(parsed_features[feature])
