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
  "features": [{
      "name": "Feature.multiStrategies.A",
      "description": "Enabled for via last stratgy",
      "enabled": true,
      "strategies": [{
          "name": "gradualRolloutRandom",
          "parameters": {
            "percentage": "0"
          }
        },
        {
          "name": "default",
          "parameters": {}
        }
      ]
    },
    {
      "name": "Feature.multiStrategies.B",
      "description": "Enabled for user=123",
      "enabled": true,
      "strategies": [{
          "name": "gradualRolloutRandom",
          "parameters": {
            "percentage": "0"
          }
        },
        {
          "name": "userWithId",
          "parameters": {
            "userIds": "123"
          }
        }
      ]
    },
    {
      "name": "Feature.multiStrategies.C",
      "description": "Enabled for user=123",
      "enabled": true,
      "strategies": [{
          "name": "gradualRolloutRandom",
          "parameters": {
            "percentage": "0"
          }
        },
        {
          "name": "userWithId",
          "parameters": {
            "userIds": "123"
          }
        },
        {
          "name": "gradualRolloutRandom",
          "parameters": {
            "percentage": "0"
          }
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
def test_feature_multiStrategies_a_enabled(unleash_client):
    """
    Feature.multiStrategies.A should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.multiStrategies.A")


@responses.activate
def test_feature_multiStrategies_b_nouser(unleash_client):
    """
    Feature.multiStrategies.B disabled for unknown user
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context = {}

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.multiStrategies.B", context)


@responses.activate
def test_feature_multiStrategies_b_enabled(unleash_client):
    """
    Feature.multiStrategies.B enabled for user=123
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context = {
        "userId": "123"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.multiStrategies.B", context)


@responses.activate
def test_feature_multiStrategies_c_unknown(unleash_client):
    """
    Feature.multiStrategies.C disabled for unknown users
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context = {}

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.multiStrategies.C", context)


@responses.activate
def test_feature_multiStrategies_c_disabled(unleash_client):
    """
    Feature.multiStrategies.C disabled for user=22
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context = {
        "userId": "22"
    }

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.multiStrategies.C", context)


@responses.activate
def test_feature_multiStrategies_c_enabled(unleash_client):
    """
    Feature.multiStrategies.C enabled for user=123
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context = {
        "userId": "123"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.multiStrategies.C", context)
