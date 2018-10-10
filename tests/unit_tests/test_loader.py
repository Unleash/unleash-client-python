import copy
import pytest
from fcache.cache import FileCache
from UnleashClient.loader import load_features
from UnleashClient.features import Feature
from UnleashClient.strategies import GradualRolloutUserId
from tests.utilities.mocks.mock_all_features import MOCK_ALL_FEATURES

MOCK_UPDATED = copy.deepcopy(MOCK_ALL_FEATURES)
MOCK_UPDATED["features"][4]["strategies"][0]["parameters"]["percentage"] = 60


@pytest.fixture()
def temp_cache():
    temporary_cache = FileCache('pytest')
    yield temporary_cache
    temporary_cache.delete()


def test_loader_initialization(temp_cache):
    in_memory_features = {}
    load_features(temp_cache, MOCK_ALL_FEATURES, in_memory_features)
    assert temp_cache["GradualRolloutUserID"]["strategies"][0]["parameters"]["percentage"] == 50
    assert isinstance(in_memory_features["GradualRolloutUserID"], Feature)
    assert isinstance(in_memory_features["GradualRolloutUserID"].strategies[0], GradualRolloutUserId)


def test_loader_refresh(temp_cache):
    in_memory_features = {}
    load_features(temp_cache, MOCK_ALL_FEATURES, in_memory_features)
    load_features(temp_cache, MOCK_UPDATED, in_memory_features)

    assert in_memory_features["GradualRolloutUserID"].strategies[0].parameters["percentage"] == 60
