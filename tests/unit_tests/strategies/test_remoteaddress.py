import pytest
from UnleashClient.strategies import RemoteAddress
from tests.utilities.testing_constants import IP_LIST


@pytest.fixture()
def strategy():
    yield RemoteAddress(parameters={"IPs": IP_LIST})


def test_ipv4_range(strategy):
    assert strategy(context={"remoteAddress": "69.208.0.1"})


def test_ipv4_value(strategy):
    assert strategy(context={"remoteAddress": "70.208.1.1"})


def test_ipv6_rangee(strategy):
    assert strategy(context={"remoteAddress": "2001:db8:1234:0000:0000:0000:0000:0001"})


def test_ipv6_value(strategy):
    assert strategy(context={"remoteAddress": "2002:db8:1234:0000:0000:0000:0000:0001"})


def test_garbage_value(strategy):
    assert not strategy(context={"remoteAddress": "WTFISTHISURCRAZY"})
