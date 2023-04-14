import pytest

from tests.utilities import generate_email_list
from UnleashClient.strategies import UserWithId

(EMAIL_LIST, CONTEXT) = generate_email_list(20)


@pytest.fixture()
def strategy():
    yield UserWithId(parameters={"userIds": EMAIL_LIST})


def test_userwithid(strategy):
    assert strategy.execute(context=CONTEXT)


def test_userwithid_missing_parameter(strategy):
    assert not strategy.execute(context={})
