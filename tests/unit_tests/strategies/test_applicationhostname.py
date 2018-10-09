import pytest
import platform
from UnleashClient.strategies import ApplicationHostname


@pytest.fixture()
def strategy():
    yield ApplicationHostname(name="Generic",
                              enabled=True,
                              parameters={"hostNames": "%s,garbage,garbage2" % platform.node()})


def test_applicationhostname(strategy):
    assert strategy()
    assert strategy.yes_count == 1
    strategy.reset_stats()
    assert strategy.yes_count == 0
