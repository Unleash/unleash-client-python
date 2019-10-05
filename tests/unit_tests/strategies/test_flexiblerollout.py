from UnleashClient.strategies.schemas import FlexibleRolloutSchema

BASE_FLEXIBLE_ROLLOUT_DICT = \
    {
        "name": "flexibleRollout",
        "parameters": {
            "rollout": 50,
            "stickiness": "userId",
            "groupId": "AB12A"
        },
        "constraints": [
            {
                "contextName": "environment",
                "operator": "IN",
                "values": [
                    "staging",
                    "prod"
                ]
            },
            {
                "contextName": "userId",
                "operator": "IN",
                "values": [
                    "122",
                    "155",
                    "9"
                ]
            },
            {
                "contextName": "userId",
                "operator": "NOT_IN",
                "values": [
                    "4"
                ]
            },
            {
                "contextName": "appName",
                "operator": "IN",
                "values": [
                    "test"
                ]
            }
        ]
    }

SCHEMA = FlexibleRolloutSchema()


def test_flexiblerollout_satisfiesconstraints():
    context = {
        'userId': "122",
        'appName': 'test',
        'environment': 'prod'
    }

    strategy = SCHEMA.load(BASE_FLEXIBLE_ROLLOUT_DICT)
    assert strategy(context)


def test_flexiblerollout_doesntsatisfiesconstraints():
    context = {
        'userId': "2",
        'appName': 'qualityhamster',
        'environment': 'prod'
    }

    strategy = SCHEMA.load(BASE_FLEXIBLE_ROLLOUT_DICT)
    assert not strategy(context)


def test_flexiblerollout_userid():
    strategy = SCHEMA.load(BASE_FLEXIBLE_ROLLOUT_DICT)

    base_context = dict(appName='test', environment='prod')
    base_context['userId'] = "122"
    assert strategy(base_context)
    base_context['userId'] = "155"
    assert not strategy(base_context)


def test_flexiblerollout_sessionid():
    BASE_FLEXIBLE_ROLLOUT_DICT['parameters']['stickiness'] = 'sessionId'
    strategy = SCHEMA.load(BASE_FLEXIBLE_ROLLOUT_DICT)

    base_context = dict(appName='test', environment='prod', userId="9")
    base_context['sessionId'] = "122"
    assert strategy(base_context)
    base_context['sessionId'] = "155"
    assert not strategy(base_context)


def test_flexiblerollout_random():
    BASE_FLEXIBLE_ROLLOUT_DICT['parameters']['stickiness'] = 'random'
    strategy = SCHEMA.load(BASE_FLEXIBLE_ROLLOUT_DICT)

    base_context = dict(appName='test', environment='prod', userId="1")
    assert strategy(base_context) in [True, False]


def test_flexiblerollout_default():
    BASE_FLEXIBLE_ROLLOUT_DICT['parameters']['stickiness'] = 'default'
    BASE_FLEXIBLE_ROLLOUT_DICT['constraints'] = [x for x in BASE_FLEXIBLE_ROLLOUT_DICT['constraints'] if x['contextName'] != 'userId']
    strategy = SCHEMA.load(BASE_FLEXIBLE_ROLLOUT_DICT)

    base_context = dict(appName='test', environment='prod', userId="122", sessionId="155")
    assert strategy(base_context)
    base_context = dict(appName='test', environment='prod', sessionId="122")
    assert strategy(base_context)
    base_context = dict(appName='test', environment='prod')
    assert strategy(base_context) in [True, False]
