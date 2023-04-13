import pytest

from tests.utilities import generate_context
from UnleashClient.strategies import GradualRolloutUserId


@pytest.fixture()
def strategy():
    yield GradualRolloutUserId(parameters={"percentage": 50, "groupId": "test"})


def test_userwithid(strategy):
    strategy.execute(context=generate_context())
