import pytest

from tests.utilities.testing_constants import IP_LIST
from UnleashClient.strategies import RemoteAddress


@pytest.fixture()
def strategy():
    yield RemoteAddress(parameters={"IPs": IP_LIST})


def test_init_with_bad_address():
    BAD_IP_LIST = IP_LIST + ",garbage"
    strategy = RemoteAddress(parameters={"IPs": BAD_IP_LIST})
    assert len(strategy.parsed_provisioning) == 4


def test_init_with_bad_range():
    BAD_IP_LIST = IP_LIST + ",ga/rbage"
    strategy = RemoteAddress(parameters={"IPs": BAD_IP_LIST})
    assert len(strategy.parsed_provisioning) == 4


def test_ipv4_range(strategy):
    assert strategy.execute(context={"remoteAddress": "69.208.0.1"})


def test_ipv4_value(strategy):
    assert strategy.execute(context={"remoteAddress": "70.208.1.1"})


def test_ipv6_rangee(strategy):
    assert strategy.execute(
        context={"remoteAddress": "2001:db8:1234:0000:0000:0000:0000:0001"}
    )


def test_ipv6_value(strategy):
    assert strategy.execute(
        context={"remoteAddress": "2002:db8:1234:0000:0000:0000:0000:0001"}
    )


def test_garbage_value(strategy):
    assert not strategy.execute(context={"remoteAddress": "WTFISTHISURCRAZY"})
