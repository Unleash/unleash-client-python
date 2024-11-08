from typing import Optional

from UnleashClient.cache import BaseCache
from UnleashClient.constants import FAILED_STRATEGIES, FEATURES_URL
from UnleashClient.features.Feature import Feature
from UnleashClient.utils import LOGGER
from UnleashClient.variants.Variants import Variants
from yggdrasil_engine.engine import UnleashEngine


def load_features(
    cache: BaseCache,
    engine: UnleashEngine,
) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param feature_toggles: Should a JSON string containing the feature toggles, equivalent to the response from Unleash API
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

    warnings = engine.take_state(feature_provisioning)
    if warnings:
        LOGGER.warning(
            "Some features were not able to be parsed correctly, they may not evaluate as expected"
        )
        LOGGER.warning(warnings)

    # # Parse provisioning
    # parsed_features = {}
    # feature_names = [d["name"] for d in feature_provisioning["features"]]

    # if "segments" in feature_provisioning.keys():
    #     segments = feature_provisioning["segments"]
    #     global_segments = {segment["id"]: segment for segment in segments}
    # else:
    #     global_segments = {}

    # for provisioning in feature_provisioning["features"]:
    #     parsed_features[provisioning["name"]] = provisioning

    # # Delete old features/cache
    # for feature in list(feature_toggles.keys()):
    #     if feature not in feature_names:
    #         del feature_toggles[feature]

    # # Update existing objects
    # for feature in feature_toggles.keys():
    #     feature_for_update = feature_toggles[feature]
    #     strategies = parsed_features[feature]["strategies"]

    #     feature_for_update.enabled = parsed_features[feature]["enabled"]
    #     if strategies:
    #         parsed_strategies = _create_strategies(
    #             parsed_features[feature], strategy_mapping, cache, global_segments
    #         )
    #         feature_for_update.strategies = parsed_strategies

    #     if "variants" in parsed_features[feature]:
    #         feature_for_update.variants = Variants(
    #             parsed_features[feature]["variants"], parsed_features[feature]["name"]
    #         )

    #     feature_for_update.impression_data = parsed_features[feature].get(
    #         "impressionData", False
    #     )

    #     feature_for_update.dependencies = parsed_features[feature].get(
    #         "dependencies", []
    #     )

    #     # If the feature had previously been added to the features list only for
    #     # tracking, indicate that it is now a real feature that should be
    #     # evaluated properly.
    #     feature_for_update.only_for_metrics = False

    # # Handle creation or deletions
    # new_features = list(set(feature_names) - set(feature_toggles.keys()))

    # for feature in new_features:
    #     feature_toggles[feature] = _create_feature(
    #         parsed_features[feature], strategy_mapping, cache, global_segments
    #     )
