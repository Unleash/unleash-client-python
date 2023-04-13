import uuid

import pytest

from UnleashClient.strategies import GradualRolloutSessionId


def generate_context():
    return {"sessionId": uuid.uuid4()}


@pytest.fixture()
def strategy():
    yield GradualRolloutSessionId(parameters={"percentage": 50, "groupId": "test"})


def test_userwithid(strategy):
    strategy.execute(context=generate_context())
