import platform

import pytest

from UnleashClient.strategies import ApplicationHostname


@pytest.fixture()
def strategy():
    yield ApplicationHostname(
        parameters={"hostNames": "%s,garbage,garbage2" % platform.node()}
    )


def test_applicationhostname(strategy):
    assert strategy.execute()


def test_applicationhostname_nomatch():
    nomatch_strategy = ApplicationHostname(parameters={"hostNames": "garbage,garbage2"})
    assert not nomatch_strategy.execute()
