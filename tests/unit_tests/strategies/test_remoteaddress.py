import pytest
from UnleashClient.strategies import RemoteAddress

IP_LIST = "69.208.0.0/29,70.208.1.1,2001:db8:1234::/48,2002:db8:1234:0000:0000:0000:0000:0001"


@pytest.fixture()
def strategy():
    yield RemoteAddress(name="Generic", enabled=True, parameters={"IPs": IP_LIST})


def test_ipv4_range(strategy):
    assert strategy(context={"remoteAddress": "69.208.0.1"})
    assert strategy.yes_count == 1
    strategy.reset_stats()
    assert strategy.yes_count == 0


def test_ipv4_value(strategy):
    assert strategy(context={"remoteAddress": "70.208.1.1"})
    assert strategy.yes_count == 1


def test_ipv6_rangee(strategy):
    assert strategy(context={"remoteAddress": "2001:db8:1234:0000:0000:0000:0000:0001"})
    assert strategy.yes_count == 1


def test_ipv6_value(strategy):
    assert strategy(context={"remoteAddress": "2002:db8:1234:0000:0000:0000:0000:0001"})
    assert strategy.yes_count == 1


def test_garbage_value(strategy):
    assert not strategy(context={"remoteAddress": "WTFISTHISURCRAZY"})
    assert strategy.no_count == 1


@pytest.mark.skip("Performance test")
def test_userwithid_timing(strategy, benchmark):
    benchmark(strategy, context={"remoteAddress": "2002:db8:1234:0000:0000:0000:0000:0001"})
