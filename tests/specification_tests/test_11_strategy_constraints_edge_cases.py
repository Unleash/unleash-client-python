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
            "name": "Feature.constraints.no_values",
            "description": "Not enabled with constraints and no values",
            "enabled": true,
            "strategies": [
                {
                    "name": "default",
                    "parameters": {},
                    "constraints": [
                        {
                            "contextName": "environment",
                            "operator": "IN",
                            "values": []

                        }
                    ]
                }
            ]
        },
        {
            "name": "Feature.constraints.no_values_NOT_IN",
            "description": "Is enabled with constraints and NOT_IN empty values",
            "enabled": true,
            "strategies": [
                {
                    "name": "default",
                    "parameters": {},
                    "constraints": [
                        {
                            "contextName": "environment",
                            "operator": "NOT_IN",
                            "values": []

                        }
                    ]
                }
            ]
        },
        {
            "name": "Feature.constraints.empty",
            "description": "Is enabled with empty constraints array",
            "enabled": true,
            "strategies": [
                {
                    "name": "default",
                    "parameters": {},
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
def test_feature_constraints_novalue_defaultenv(unleash_client):
    """
    Feature.constraints.no_value should not be enabled in default environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.constraints.no_values", {'environment': 'default'})


@responses.activate
def test_feature_constraints_novalue_emptyenv(unleash_client):
    """
    Feature.constraints.no_value should not be enabled in empty environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.constraints.no_values", {})


@responses.activate
def test_feature_constraints_novalue_defaultenv_notin(unleash_client):
    """
    Feature.constraints.no_values_NOT_IN should be enabled in default environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.constraints.no_values_NOT_IN", {'environment': 'default'})


@responses.activate
def test_feature_constraints_novalue_emptyenv_notin(unleash_client):
    """
    Feature.constraints.no_values_NOT_IN should be enabled in empty environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.constraints.no_values_NOT_IN", {})


@responses.activate
def test_feature_constraints_empty_defaultenv(unleash_client):
    """
    Feature.constraints.empty should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.constraints.no_values_NOT_IN", {'environment': 'default'})


@responses.activate
def test_feature_constraints_empty_emptyenv(unleash_client):
    """
    Feature.constraints.empty should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.constraints.no_values_NOT_IN", {})