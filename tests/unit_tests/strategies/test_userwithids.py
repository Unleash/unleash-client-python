import pytest
from tests.utilities import generate_email_list
from UnleashClient.strategies import UserWithId

(EMAIL_LIST, CONTEXT) = generate_email_list(20)


@pytest.fixture()
def strategy():
    yield UserWithId(name="Generic", enabled=True, parameters={"userIds": EMAIL_LIST})


def test_userwithid(strategy):
    assert strategy(context=CONTEXT)
    assert strategy.yes_count == 1
    strategy.reset_stats()
    assert strategy.yes_count == 0


def test_userwithid_distribution(strategy):
    for _ in range(100):
        strategy(context=CONTEXT)

    assert strategy.yes_count == 100


@pytest.mark.skip("Performance test")
def test_userwithid_timing(strategy, benchmark):
    benchmark(strategy, CONTEXT)
