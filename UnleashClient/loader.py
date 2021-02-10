from fcache.cache import FileCache
from UnleashClient.features.Feature import Feature
from UnleashClient.variants.Variants import Variants
from UnleashClient.constants import FEATURES_URL, FAILED_STRATEGIES
from UnleashClient.utils import LOGGER


# pylint: disable=broad-except
def _create_strategies(provisioning: dict,
                       strategy_mapping: dict,
                       cache: FileCache) -> list:
    feature_strategies = []

    for strategy in provisioning["strategies"]:
        try:
            if "parameters" in strategy.keys():
                strategy_provisioning = strategy['parameters']
            else:
                strategy_provisioning = {}

            if "constraints" in strategy.keys():
                constraint_provisioning = strategy['constraints']
            else:
                constraint_provisioning = {}

            feature_strategies.append(strategy_mapping[strategy['name']](
                constraints=constraint_provisioning, parameters=strategy_provisioning
            ))
        except Exception as excep:
            if FAILED_STRATEGIES not in cache.keys():
                cache[FAILED_STRATEGIES] = []  # Initialize cache key only if failures exist.

            if strategy['name'] not in cache[FAILED_STRATEGIES]:
                LOGGER.warning("Failed to load strategy. This may be a problem with a custom strategy. Exception: %s", excep)
                cache[FAILED_STRATEGIES].append(strategy['name'])

    return feature_strategies


def _create_feature(provisioning: dict,
                    strategy_mapping: dict,
                    cache: FileCache) -> Feature:
    if "strategies" in provisioning.keys():
        parsed_strategies = _create_strategies(provisioning, strategy_mapping, cache)
    else:
        parsed_strategies = []

    if "variants" in provisioning:
        variant = Variants(provisioning['variants'], provisioning['name'])
    else:
        variant = None

    return Feature(name=provisioning["name"],
                   enabled=provisioning["enabled"],
                   strategies=parsed_strategies,
                   variants=variant
                   )


def load_features(cache: FileCache,
                  feature_toggles: dict,
                  strategy_mapping: dict) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param feature_toggles: Should be the features class variable from UnleashClient
    :param strategy_mapping:
    :return:
    """
    # Pull raw provisioning from cache.
    try:
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
                parsed_strategies = _create_strategies(parsed_features[feature], strategy_mapping, cache)
                feature_for_update.strategies = parsed_strategies

            if 'variants' in parsed_features[feature]:
                feature_for_update.variants = Variants(
                    parsed_features[feature]['variants'],
                    parsed_features[feature]['name']
                )

        # Handle creation or deletions
        new_features = list(set(feature_names) - set(feature_toggles.keys()))

        for feature in new_features:
            feature_toggles[feature] = _create_feature(parsed_features[feature], strategy_mapping, cache)
    except KeyError as cache_exception:
        LOGGER.warning("Cache Exception: %s", cache_exception)
        LOGGER.warning("Unleash client does not have cached features. "
                       "Please make sure client can communicate with Unleash server!")
