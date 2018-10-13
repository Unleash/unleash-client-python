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
      "name": "Feature.remoteAddress.A",
      "description": "Enabled toggle for localhost",
      "enabled": true,
      "strategies": [{
        "name": "remoteAddress",
        "parameters": {
          "IPs": "127.0.0.1"
        }
      }]
    },
    {
      "name": "Feature.remoteAddress.B",
      "description": "Enabled toggle for list of IPs",
      "enabled": true,
      "strategies": [{
        "name": "remoteAddress",
        "parameters": {
          "IPs": "192.168.0.1, 192.168.0.2, 192.168.0.3"
        }
      }]
    },
    {
      "name": "Feature.remoteAddress.C",
      "description": "Ignore invalid IP's in list",
      "enabled": true,
      "strategies": [{
        "name": "remoteAddress",
        "parameters": {
          "IPs": "192.168.0.1, 192.invalid, 192.168.0.2, 192.168.0.3"
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
def test_feature_remoteaddress_a_enabled(unleash_client):
    """
    Feature.remoteAddress.A should be enabled for localhost
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "remoteAddress": "127.0.0.1"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.remoteAddress.A", context_values)


@responses.activate
def test_feature_remoteaddress_a_nocontext(unleash_client):
    """
    Feature.remoteAddress.A should not be enabled for missing remoteAddress on context
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {}

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.remoteAddress.A", context_values)


@responses.activate
def test_feature_remoteaddress_b_enabled(unleash_client):
    """
    Feature.remoteAddress.B should be enabled for remoteAddress 192.168.0.1
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "remoteAddress": "192.168.0.1"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.remoteAddress.B", context_values)


@responses.activate
def test_feature_remoteaddress_b_list(unleash_client):
    """
    Feature.remoteAddress.B should be enabled for remoteAddress 192.168.0.3
    TODO: Error in spec.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "remoteAddress": "192.168.0.3"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.remoteAddress.B", context_values)


@responses.activate
def test_feature_remoteaddress_b_notlist(unleash_client):
    """
    Feature.remoteAddress.B should not be enabled for remoteAddress 217.100.10.11
    TODO: Error in spec.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "remoteAddress": "217.100.10.11"
    }

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.remoteAddress.B", context_values)


@responses.activate
def test_feature_remoteaddress_c(unleash_client):
    """
    Feature.remoteAddress.C should be enabled for remoteAddress 192.168.0.3
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "remoteAddress": "192.168.0.3"
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.remoteAddress.C", context_values)
