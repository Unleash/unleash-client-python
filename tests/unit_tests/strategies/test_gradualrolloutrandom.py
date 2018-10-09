from math import isclose
import pytest
from UnleashClient.strategies import GradualRolloutRandom


@pytest.fixture()
def strategy():
    yield GradualRolloutRandom(name="Generic", enabled=True, parameters={"percentage": 50})


def test_userwithid(strategy):
    strategy()
    assert strategy.yes_count == 1 or strategy.no_count == 1
    strategy.reset_stats()
    assert strategy.yes_count == 0 and strategy.no_count == 0


def test_userwithid_distribution(strategy):
    for _ in range(1000):
        strategy()

    assert isclose(strategy.yes_count, 500, abs_tol=50)


@pytest.mark.skip("Performance test")
def test_userwithid_timing(strategy, benchmark):
    benchmark(strategy)
