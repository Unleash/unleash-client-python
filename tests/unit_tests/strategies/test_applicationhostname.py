import pytest
import platform
from UnleashClient.strategies import ApplicationHostname


@pytest.fixture()
def strategy():
    yield ApplicationHostname(parameters={"hostNames": "%s,garbage,garbage2" % platform.node()})


def test_applicationhostname(strategy):
    assert strategy()
