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
      "name": "Feature.A3",
      "description": "Enabled toggle for 100%",
      "enabled": true,
      "strategies": [{
        "name": "gradualRolloutUserId",
        "parameters": {
          "percentage": "100",
          "groupId": "AB12A"
        }
      }]
    },
    {
      "name": "Feature.B3",
      "description": "Enabled toggle for 50%",
      "enabled": true,
      "strategies": [{
        "name": "gradualRolloutUserId",
        "parameters": {
          "percentage": "50",
          "groupId": "AB12A"
        }
      }]
    },
    {
      "name": "Feature.C3",
      "enabled": true,
      "strategies": [{
        "name": "gradualRolloutUserId",
        "parameters": {
          "percentage": "0",
          "groupId": "AB12A"
        }
      }]
    },
    {
      "name": "Feature.D3",
      "enabled": true,
      "strategies": [{
          "name": "gradualRolloutUserId",
          "parameters": {
            "percentage": "0",
            "groupId": "AB12A"
          }
        },
        {
          "name": "default"
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
def test_feature_a3_enabled(unleash_client):
    """
    Feature.A3 should be enabled for user on context
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
    assert unleash_client.is_enabled("Feature.A3", context_values)


@responses.activate
def test_feature_a3_nocontext(unleash_client):
    """
    Feature.A3 should be disabled when no user on context
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {}

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.A3", context_values)


@responses.activate
def test_feature_b3_enabled(unleash_client):
    """
    Feature.B3 should be enabled for userId=122
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "122"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.B3", context_values)


@responses.activate
def test_feature_b3_disabled(unleash_client):
    """
    Feature.B3 should be disabled for userId=155
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "155"
    }

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.B3", context_values)


@responses.activate
def test_feature_c3(unleash_client):
    """
    Feature.C3 should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "122"
    }

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.C3", context_values)


@responses.activate
def test_feature_d3(unleash_client):
    """
    Feature.D3 should be enabled for all because of default strategy
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "122"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.D3", context_values)
