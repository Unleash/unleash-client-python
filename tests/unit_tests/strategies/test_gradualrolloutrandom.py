import pytest

from UnleashClient.strategies import GradualRolloutRandom


@pytest.fixture()
def strategy():
    yield GradualRolloutRandom(parameters={"percentage": 50})


def test_userwithid(strategy):
    assert isinstance(strategy.execute(), bool)
