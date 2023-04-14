import pytest

from UnleashClient.strategies import Default


@pytest.fixture()
def strategy():
    yield Default()


def test_defaultstrategy(strategy):
    assert isinstance(strategy.execute(), bool)
