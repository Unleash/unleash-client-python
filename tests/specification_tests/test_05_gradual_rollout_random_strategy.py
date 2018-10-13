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
      "name": "Feature.A5",
      "description": "Enabled toggle for 100%",
      "enabled": true,
      "strategies": [{
        "name": "gradualRolloutRandom",
        "parameters": {
          "percentage": "100"
        }
      }]
    },
    {
      "name": "Feature.B5",
      "description": "Disabled toggle with 0% rollout",
      "enabled": true,
      "strategies": [{
        "name": "gradualRolloutRandom",
        "parameters": {
          "percentage": "0"
        }
      }]
    },
    {
      "name": "Feature.C5",
      "enabled": true,
      "strategies": [{
          "name": "gradualRolloutRandom",
          "parameters": {
            "percentage": "0"
          }
        },
        {
          "name": "default"
        }
      ]
    },
    {
      "name": "Feature.D5",
      "description": "Disabled toggle should be disabled",
      "enabled": false,
      "strategies": [{
        "name": "gradualRolloutRandom",
        "parameters": {
          "percentage": "100"
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
def test_feature_a5(unleash_client):
    """
    Feature.A5 should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.A5")


@responses.activate
def test_feature_b5(unleash_client):
    """
    Feature.B5 should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.B5")


@responses.activate
def test_feature_c5(unleash_client):
    """
    Feature.C5 should be enabled because of default strategy
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.C5")


@responses.activate
def test_feature_d5(unleash_client):
    """
    Feature.D5 should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.D5")
