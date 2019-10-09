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
      "name": "Feature.flexibleRollout.100",
      "description": "Should be enabled",
      "enabled": true,
      "strategies": [
        {
          "name": "flexibleRollout",
          "parameters": {
            "rollout": "100",
            "stickiness": "default",
            "groupId": "Feature.flexibleRollout.100"
          },
          "constraints": []
        }
      ]
    },
    {
      "name": "Feature.flexibleRollout.10",
      "description": "Should be enabled",
      "enabled": true,
      "strategies": [
        {
          "name": "flexibleRollout",
          "parameters": {
            "rollout": "10",
            "stickiness": "default",
            "groupId": "Feature.flexibleRollout.10"
          },
          "constraints": []
        }
      ]
    },
    {
      "name": "Feature.flexibleRollout.userId.55",
      "description": "Should be enabled",
      "enabled": true,
      "strategies": [
        {
          "name": "flexibleRollout",
          "parameters": {
            "rollout": "55",
            "stickiness": "userId",
            "groupId": "Feature.flexibleRollout.userId.55"
          },
          "constraints": []
        }
      ]
    },
    {
      "name": "Feature.flexibleRollout.sessionId.42",
      "description": "Should be enabled",
      "enabled": true,
      "strategies": [
        {
          "name": "flexibleRollout",
          "parameters": {
            "rollout": "42",
            "stickiness": "sessionId",
            "groupId": "Feature.flexibleRollout.sessionId.42"
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
def test_feature_100_enabled(unleash_client):
    """
    Feature.flexibleRollout.100 should always be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexibleRollout.100", {})


@responses.activate
def test_feature_10userid_enabled(unleash_client):
    """
    Feature.flexibleRollout.10 should be enabled for userId=174
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexibleRollout.10", {"userId": "174"})


@responses.activate
def test_feature_10userid_disabled(unleash_client):
    """
    Feature.flexibleRollout.10 should be disabled for userId=499
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.flexibleRollout.10", {"userId": "499"})


@responses.activate
def test_feature_10sessionid_enabled(unleash_client):
    """
    Feature.flexibleRollout.10 should be enabled for sessionId=174
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexibleRollout.10", {"sessionId": "174"})


@responses.activate
def test_feature_10sessionid_disabled(unleash_client):
    """
    Feature.flexibleRollout.10 should be disabled for sessionId=499
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.flexibleRollout.10", {"userId": "499"})


@responses.activate
def test_feature_55userid_enabled(unleash_client):
    """
    Feature.flexibleRollout.userId.55 should be enabled for userId=25
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexibleRollout.userId.55", {"userId": "25"})


@responses.activate
def test_feature_55sessionid_disabled(unleash_client):
    """
    Feature.flexibleRollout.userId.55 should be disabled for sessionId=25
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.flexibleRollout.userId.55", {"sessionId": "25"})


@responses.activate
def test_feature_55_nouserdisabled(unleash_client):
    """
    Feature.flexibleRollout.userId.55 should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.flexibleRollout.userId.55", {})


@responses.activate
def test_feature_42sessionid_enabled(unleash_client):
    """
    Feature.flexibleRollout.sessionId.42 should be enabled for sessionId=147
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.flexibleRollout.sessionId.42", {"sessionId": "147"})
