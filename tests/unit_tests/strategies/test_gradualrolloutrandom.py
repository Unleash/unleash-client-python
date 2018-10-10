import pytest
from UnleashClient.strategies import GradualRolloutRandom


@pytest.fixture()
def strategy():
    yield GradualRolloutRandom(parameters={"percentage": 50})


def test_userwithid(strategy):
    assert isinstance(strategy(), bool)


def test_object_eq():
    gr1 = GradualRolloutRandom(parameters={"percentage": 50})
    gr2 = GradualRolloutRandom(parameters={"percentage": 60})
    gr3 = GradualRolloutRandom(parameters={"percentage": 50})

    assert not gr1 == gr2
    assert gr1 == gr3
