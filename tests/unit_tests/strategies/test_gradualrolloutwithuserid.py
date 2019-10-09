import pytest
from UnleashClient.strategies import GradualRolloutUserId
from tests.utilities import generate_context


@pytest.fixture()
def strategy():
    yield GradualRolloutUserId(parameters={"percentage": 50, "groupId": "test"})


def test_userwithid(strategy):
    strategy.execute(context=generate_context())
