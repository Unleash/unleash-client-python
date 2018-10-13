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
      "name": "Feature.A2",
      "description": "Enabled toggle",
      "enabled": true,
      "strategies": [{
        "name": "userWithId",
        "parameters": {
          "userIds": "123"
        }
      }]
    },
    {
      "name": "Feature.B2",
      "description": "Disabled toggle",
      "enabled": true,
      "strategies": [{
        "name": "userWithId",
        "parameters": {
          "userIds": "123"
        }
      }]
    },
    {
      "name": "Feature.C2",
      "enabled": true,
      "strategies": [{
          "name": "userWithId",
          "parameters": {
            "userIds": "123"
          }
        },
        {
          "name": "default"
        }
      ]
    },
    {
      "name": "Feature.D2",
      "enabled": true,
      "strategies": [{
        "name": "userWithId",
        "parameters": {
          "userIds": "123, 222, 88"
        }
      }]
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
def test_feature_a2_enabled(unleash_client):
    """
    Feature.A2 Should be enabled for user on context
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "123"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.A2", context_values)


@responses.activate
def test_feature_a2_disabled(unleash_client):
    """
    Feature.A2 Should not be enabled for user not in context
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "22"
    }

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.A2", context_values)


@responses.activate
def test_feature_c2(unleash_client):
    """
    Feature.C2 Should not be "disabled" for for everyone
    TODO: Contact team about issue in test case description, should be enabled.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "22"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.C2", context_values)


@responses.activate
def test_feature_d2(unleash_client):
    """
    Feature.D2 Should "-not-" be enabled for user in list
    TODO: Contact team about issue in test case description, should be enabled.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "222"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.D2", context_values)


@responses.activate
def test_feature_no_id(unleash_client):
    """
    Feature.A2 Should be disabled when no userId on context
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {}

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.A2", context_values)
