from typing import Optional

from UnleashClient.cache import BaseCache
from UnleashClient.constants import FAILED_STRATEGIES, FEATURES_URL
from UnleashClient.features.Feature import Feature
from UnleashClient.utils import LOGGER
from UnleashClient.variants.Variants import Variants


# pylint: disable=broad-except
def _create_strategies(
    provisioning: dict,
    strategy_mapping: dict,
    cache: BaseCache,
    global_segments: Optional[dict],
) -> list:
    feature_strategies = []

    for strategy in provisioning["strategies"]:
        try:
            if "parameters" in strategy.keys():
                strategy_provisioning = strategy["parameters"]
            else:
                strategy_provisioning = {}

            if "constraints" in strategy.keys():
                constraint_provisioning = strategy["constraints"]
            else:
                constraint_provisioning = {}

            if "segments" in strategy.keys():
                segment_provisioning = strategy["segments"]
            else:
                segment_provisioning = []

            if "variants" in strategy.keys():
                variant_provisioning = strategy["variants"]
            else:
                variant_provisioning = []

            feature_strategies.append(
                strategy_mapping[strategy["name"]](
                    constraints=constraint_provisioning,
                    variants=variant_provisioning,
                    parameters=strategy_provisioning,
                    global_segments=global_segments,
                    segment_ids=segment_provisioning,
                )
            )
        except Exception as excep:
            strategies = cache.get(FAILED_STRATEGIES, [])

            if strategy["name"] not in strategies:
                LOGGER.warning(
                    "Failed to load strategy. This may be a problem with a custom strategy. Exception: %s",
                    excep,
                )
                strategies.append(strategy["name"])

            cache.set(FAILED_STRATEGIES, strategies)

    return feature_strategies


def _create_feature(
    provisioning: dict,
    strategy_mapping: dict,
    cache: BaseCache,
    global_segments: Optional[dict],
) -> Feature:
    if "strategies" in provisioning.keys():
        parsed_strategies = _create_strategies(
            provisioning, strategy_mapping, cache, global_segments
        )
    else:
        parsed_strategies = []

    if "variants" in provisioning:
        variant = Variants(provisioning["variants"], provisioning["name"])
    else:
        variant = None

    return Feature(
        name=provisioning["name"],
        enabled=provisioning["enabled"],
        strategies=parsed_strategies,
        variants=variant,
        impression_data=provisioning.get("impressionData", False),
        dependencies=provisioning.get("dependencies", []),
    )


def load_features(
    cache: BaseCache,
    feature_toggles: dict,
    strategy_mapping: dict,
    global_segments: Optional[dict] = None,
) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param feature_toggles: Should be the features class variable from UnleashClient
    :param strategy_mapping:
    :return:
    """
    # Pull raw provisioning from cache.
    feature_provisioning = cache.get(FEATURES_URL)
    if not feature_provisioning:
        LOGGER.warning(
            "Unleash client does not have cached features. "
            "Please make sure client can communicate with Unleash server!"
        )
        return

    # Parse provisioning
    parsed_features = {}
    feature_names = [d["name"] for d in feature_provisioning["features"]]

    if "segments" in feature_provisioning.keys():
        segments = feature_provisioning["segments"]
        global_segments = {segment["id"]: segment for segment in segments}
    else:
        global_segments = {}

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
            parsed_strategies = _create_strategies(
                parsed_features[feature], strategy_mapping, cache, global_segments
            )
            feature_for_update.strategies = parsed_strategies

        if "variants" in parsed_features[feature]:
            feature_for_update.variants = Variants(
                parsed_features[feature]["variants"], parsed_features[feature]["name"]
            )

        feature_for_update.impression_data = parsed_features[feature].get(
            "impressionData", False
        )

        feature_for_update.dependencies = parsed_features[feature].get(
            "dependencies", []
        )

        # If the feature had previously been added to the features list only for
        # tracking, indicate that it is now a real feature that should be
        # evaluated properly.
        feature_for_update.only_for_metrics = False

    # Handle creation or deletions
    new_features = list(set(feature_names) - set(feature_toggles.keys()))

    for feature in new_features:
        feature_toggles[feature] = _create_feature(
            parsed_features[feature], strategy_mapping, cache, global_segments
        )
