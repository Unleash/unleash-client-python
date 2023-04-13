import pytest

from UnleashClient.strategies.FlexibleRolloutStrategy import FlexibleRollout

BASE_FLEXIBLE_ROLLOUT_DICT = {
    "name": "flexibleRollout",
    "parameters": {"rollout": 50, "stickiness": "userId", "groupId": "AB12A"},
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
    )


def test_flexiblerollout_satisfiesconstraints(strategy):
    context = {"userId": "122", "appName": "test", "environment": "prod"}

    assert strategy.execute(context)


def test_flexiblerollout_doesntsatisfiesconstraints(strategy):
    context = {"userId": "2", "appName": "qualityhamster", "environment": "prod"}
    assert not strategy.execute(context)


def test_flexiblerollout_userid(strategy):
    base_context = dict(appName="test", environment="prod")
    base_context["userId"] = "122"
    assert strategy.execute(base_context)
    base_context["userId"] = "155"
    assert not strategy.execute(base_context)


def test_flexiblerollout_sessionid(strategy):
    BASE_FLEXIBLE_ROLLOUT_DICT["parameters"]["stickiness"] = "sessionId"
    base_context = dict(appName="test", environment="prod", userId="9")
    base_context["sessionId"] = "122"
    assert strategy.execute(base_context)
    base_context["sessionId"] = "155"
    assert not strategy.execute(base_context)


def test_flexiblerollout_random(strategy):
    BASE_FLEXIBLE_ROLLOUT_DICT["parameters"]["stickiness"] = "random"
    base_context = dict(appName="test", environment="prod", userId="1")
    assert strategy.execute(base_context) in [True, False]


def test_flexiblerollout_customfield(strategy):
    BASE_FLEXIBLE_ROLLOUT_DICT["parameters"]["stickiness"] = "customField"
    base_context = dict(appName="test", environment="prod", userId="9")
    base_context["customField"] = "122"
    assert strategy.execute(base_context)
    base_context["customField"] = "155"
    assert not strategy.execute(base_context)


def test_flexiblerollout_default():
    BASE_FLEXIBLE_ROLLOUT_DICT["parameters"]["stickiness"] = "default"
    BASE_FLEXIBLE_ROLLOUT_DICT["constraints"] = [
        x
        for x in BASE_FLEXIBLE_ROLLOUT_DICT["constraints"]
        if x["contextName"] != "userId"
    ]
    strategy = FlexibleRollout(
        BASE_FLEXIBLE_ROLLOUT_DICT["constraints"],
        BASE_FLEXIBLE_ROLLOUT_DICT["parameters"],
    )
    base_context = dict(
        appName="test", environment="prod", userId="122", sessionId="155"
    )
    assert strategy.execute(base_context)
    base_context = dict(appName="test", environment="prod", sessionId="122")
    assert strategy.execute(base_context)
    base_context = dict(appName="test", environment="prod")
    assert strategy.execute(base_context) in [True, False]
