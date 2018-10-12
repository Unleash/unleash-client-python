import copy
from UnleashClient.loader import load_features
from UnleashClient.features import Feature
from UnleashClient.strategies import GradualRolloutUserId
from UnleashClient.constants import FEATURES_URL
from tests.utilities.mocks.mock_all_features import MOCK_ALL_FEATURES
from tests.utilities.decorators import cache_full  # noqa: F401

MOCK_UPDATED = copy.deepcopy(MOCK_ALL_FEATURES)
MOCK_UPDATED["features"][4]["strategies"][0]["parameters"]["percentage"] = 60


def test_loader_initialization(cache_full):  # noqa: F811
    # Set up variables
    in_memory_features = {}
    temp_cache = cache_full

    # Tests
    load_features(temp_cache, in_memory_features)
    assert isinstance(in_memory_features["GradualRolloutUserID"], Feature)
    assert isinstance(in_memory_features["GradualRolloutUserID"].strategies[0], GradualRolloutUserId)


def test_loader_refresh(cache_full):  # noqa: F811
    # Set up variables
    in_memory_features = {}
    temp_cache = cache_full

    load_features(temp_cache, in_memory_features)

    # Simulate update mutation
    temp_cache[FEATURES_URL] = MOCK_UPDATED
    temp_cache.sync()

    load_features(temp_cache, in_memory_features)

    assert in_memory_features["GradualRolloutUserID"].strategies[0].parameters["percentage"] == 60
