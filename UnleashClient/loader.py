from typing import Optional

from yggdrasil_engine.engine import UnleashEngine

from UnleashClient.cache import BaseCache
from UnleashClient.constants import FAILED_STRATEGIES, FEATURES_URL
from UnleashClient.features.Feature import Feature
from UnleashClient.utils import LOGGER
from UnleashClient.variants.Variants import Variants


def load_features(
    cache: BaseCache,
    engine: UnleashEngine,
) -> None:
    """
    Caching

    :param cache: Should be the cache class variable from UnleashClient
    :param feature_toggles: Should be a JSON string containing the feature toggles, equivalent to the response from Unleash API
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
