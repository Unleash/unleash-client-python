import pytest

from tests.utilities.mocks.mock_variants import VARIANTS_WITH_STICKINESS
from UnleashClient.strategies import EvaluationResult, FlexibleRollout

BASE_FLEXIBLE_ROLLOUT_DICT = {
    "name": "flexibleRollout",
    "parameters": {"rollout": 50, "stickiness": "userId", "groupId": "AB12A"},
    "variants": VARIANTS_WITH_STICKINESS,
    "constraints": [
        {"contextName": "environment", "operator": "IN", "values": ["staging", "prod"]},
        {"contextName": "userId", "operator": "IN", "values": ["122", "155", "9"]},
        {"contextName": "userId", "operator": "NOT_IN", "values": ["4"]},
        {"contextName": "appName", "operator": "IN", "values": ["test"]},
    ],
}


@pytest.fixture()
def strategy():
    yield FlexibleRollout(
        BASE_FLEXIBLE_ROLLOUT_DICT["constraints"],
        BASE_FLEXIBLE_ROLLOUT_DICT["parameters"],
        variants=VARIANTS_WITH_STICKINESS,
    )


def test_flexiblerollout_satisfies_constraints_returns_variant(strategy):
    context = {
        "userId": "122",
        "appName": "test",
        "environment": "prod",
        "customField": "1",
    }
    result: EvaluationResult = strategy.get_result(context)
    assert result.enabled
    assert result.variant == {
        "enabled": True,
        "name": "VarC",
        "payload": {"type": "string", "value": "Test 3"},
    }


def test_flexiblerollout_does_not_satisfy_constraints_returns_default_variant(strategy):
    context = {
        "userId": "12234",
        "appName": "test2",
        "environment": "prod2",
        "customField": "1",
    }
    result: EvaluationResult = strategy.get_result(context)
    print(result)
    assert not result.enabled
    assert result.variant is None
