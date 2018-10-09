import pytest
import timeit
from UnleashClient.strategies import Default


@pytest.fixture()
def strategy():
    yield Default(name="Generic", enabled=True)


def test_defaultstrategy(strategy):
    assert strategy()
    assert strategy.yes_count == 1
    strategy.reset_stats()
    assert strategy.yes_count == 0


@pytest.mark.skip("For performance only.")
def test_defaultstrategy_distribution(strategy):
    assert timeit.timeit(strategy) < 1
    assert strategy.yes_count == 1000000
