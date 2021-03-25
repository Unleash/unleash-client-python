import uuid
import json
import pytest
import responses
from UnleashClient import UnleashClient
from UnleashClient.constants import FEATURES_URL, METRICS_URL, REGISTER_URL
from tests.utilities.testing_constants import URL, APP_NAME


MOCK_JSON = """
 {
    "version": 1,
    "features": [
        {
            "name": "Feature.flexible.rollout.custom.stickiness_100",
            "description": "Should support custom stickiness as option",
            "enabled": true,
            "strategies": [
                {
                    "name": "flexibleRollout",
                    "parameters": {
                        "rollout": "100",
                        "stickiness": "customField",
                        "groupId": "Feature.flexible.rollout.custom.stickiness_100"
                    },
                    "constraints": []
                }
            ],
            "variants": [
                {
                    "name": "blue",
                    "weight": 25,
                    "stickiness": "customField",
                    "payload": {
                        "type": "string",
                        "value": "val1"
                    }
                },
                {
                    "name": "red",
                    "weight": 25,
                    "stickiness": "customField",
                    "payload": {
                        "type": "string",
                        "value": "val1"
                    }
                },
                {
                    "name": "green",
                    "weight": 25,
                    "stickiness": "customField",
                    "payload": {
                        "type": "string",
                        "value": "val1"
                    }
                },
                {
                    "name": "yellow",
                    "weight": 25,
                    "stickiness": "customField",
                    "payload": {
                        "type": "string",
                        "value": "val1"
                    }
                }
            ]
        },
        {
            "name": "Feature.flexible.rollout.custom.stickiness_50",
            "description": "Should support custom stickiness as option",
            "enabled": true,
            "strategies": [
                {
                    "name": "flexibleRollout",
                    "parameters": {
                        "rollout": "50",
                        "stickiness": "customField",
                        "groupId": "Feature.flexible.rollout.custom.stickiness_50"
                    },
                    "constraints": []
                }
            ]
        }
    ]
}
"""


@pytest.fixture()
def unleash_client():
    unleash_client = UnleashClient(url=URL,
                                   app_name=APP_NAME,
                                   instance_id='pytest_%s' % uuid.uuid4())
    yield unleash_client
    unleash_client.destroy()


@responses.activate
def test_feature_flexiblerollout_stickiness_100(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_100 should be enabled without field defined for 100%
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexible.rollout.custom.stickiness_100", {'customField': 'any_value'})


@responses.activate
def test_feature_flexiblerollout_stickiness_50_nocontext(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_50 should not be enabled without custom field
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.flexible.rollout.custom.stickiness_50", {})


@responses.activate
def test_feature_flexiblerollout_stickiness_50_customfield_402(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_50 should not enabled without customField=402
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.flexible.rollout.custom.stickiness_50", {'customField': '402'})


@responses.activate
def test_feature_flexiblerollout_stickiness_50_customfield_388(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_50 should be enabled for customField=388
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexible.rollout.custom.stickiness_50", {'customField': '388'})


@responses.activate
def test_feature_flexiblerollout_stickiness_50_customfield_39(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_50 should be enabled without customField=39
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexible.rollout.custom.stickiness_50", {'customField': '39'})


@responses.activate
def test_variant_flexiblerollout_stickiness_100_customfield_528(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_100 and customField=528 yields blue
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'customField': "528"
    }

    expected_result = {
        "name": "blue",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    actual_result = unleash_client.get_variant("Feature.flexible.rollout.custom.stickiness_100", context)
    assert actual_result == expected_result


@responses.activate
def test_variant_flexiblerollout_stickiness_100_customfield_16(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_100 and customField=16 yields blue
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'customField': "16"
    }

    expected_result = {
        "name": "blue",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    actual_result = unleash_client.get_variant("Feature.flexible.rollout.custom.stickiness_100", context)
    assert actual_result == expected_result


@responses.activate
def test_variant_flexiblerollout_stickiness_100_customfield_198(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_100 and customField=198 yields red
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'customField': "198"
    }

    expected_result = {
        "name": "red",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    actual_result = unleash_client.get_variant("Feature.flexible.rollout.custom.stickiness_100", context)
    assert actual_result == expected_result


@responses.activate
def test_variant_flexiblerollout_stickiness_100_customfield_43(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_100 and customField=43 yields green
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'customField': "43"
    }

    expected_result = {
        "name": "green",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    actual_result = unleash_client.get_variant("Feature.flexible.rollout.custom.stickiness_100", context)
    assert actual_result == expected_result


@responses.activate
def test_variant_flexiblerollout_stickiness_100_customfield_112(unleash_client):
    """
    Feature.flexible.rollout.custom.stickiness_100 and customField=112 yields yellow
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'customField': "112"
    }

    expected_result = {
        "name": "yellow",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    actual_result = unleash_client.get_variant("Feature.flexible.rollout.custom.stickiness_100", context)
    assert actual_result == expected_result
