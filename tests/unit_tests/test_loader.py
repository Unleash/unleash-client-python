import copy
from UnleashClient.loader import load_features
from UnleashClient.features import Feature
from UnleashClient.strategies import GradualRolloutUserId, FlexibleRollout, UserWithId
from UnleashClient.variants import Variants
from UnleashClient.constants import FEATURES_URL
from tests.utilities.mocks import MOCK_ALL_FEATURES
from tests.utilities.testing_constants import DEFAULT_STRATEGY_MAPPING
from tests.utilities.decorators import cache_full, cache_custom  # noqa: F401

MOCK_UPDATED = copy.deepcopy(MOCK_ALL_FEATURES)
MOCK_UPDATED["features"][4]["strategies"][0]["parameters"]["percentage"] = 60


def test_loader_initialization(cache_full):  # noqa: F811
    # Set up variables
    in_memory_features = {}
    temp_cache = cache_full

    # Tests
    load_features(temp_cache, in_memory_features, DEFAULT_STRATEGY_MAPPING)
    assert isinstance(in_memory_features["GradualRolloutUserID"], Feature)
    assert isinstance(in_memory_features["GradualRolloutUserID"].strategies[0], GradualRolloutUserId)

    for feature_name in in_memory_features.keys():
        feature = in_memory_features[feature_name]
        assert len(feature.strategies) > 0
        strategy = feature.strategies[0]

        if isinstance(strategy, UserWithId):
            assert strategy.parameters
            assert len(strategy.parsed_provisioning)

        if isinstance(strategy, FlexibleRollout):
            len(strategy.parsed_constraints) > 0

        if isinstance(strategy, Variants):
            assert strategy.variants


def test_loader_refresh(cache_full):  # noqa: F811
    # Set up variables
    in_memory_features = {}
    temp_cache = cache_full

    load_features(temp_cache, in_memory_features, DEFAULT_STRATEGY_MAPPING)

    # Simulate update mutation
    temp_cache[FEATURES_URL] = MOCK_UPDATED
    temp_cache.sync()

    load_features(temp_cache, in_memory_features, DEFAULT_STRATEGY_MAPPING)

    assert in_memory_features["GradualRolloutUserID"].strategies[0].parameters["percentage"] == 60


def test_loader_initialization_failure(cache_custom):  # noqa: F811
    # Set up variables
    in_memory_features = {}
    temp_cache = cache_custom

    # Tests
    load_features(temp_cache, in_memory_features, DEFAULT_STRATEGY_MAPPING)
    assert isinstance(in_memory_features["UserWithId"], Feature)
