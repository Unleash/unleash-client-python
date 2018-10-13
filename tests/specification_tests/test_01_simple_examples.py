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
            "name": "Feature.A",
            "description": "Enabled toggle",
            "enabled": true,
            "strategies": [{
                "name": "default"
            }]
        },
        {
            "name": "Feature.B",
            "description": "Disabled toggle",
            "enabled": false,
            "strategies": [{
                "name": "default"
            }]
        },
        {
            "name": "Feature.C",
            "enabled": true,
            "strategies": []
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
def test_feature_a(unleash_client):
    """
    Feature.A should be enabled.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.A")


@responses.activate
def test_feature_b(unleash_client):
    """
    Feature.B should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.B")


@responses.activate
def test_feature_c(unleash_client):
    """
    Feature.C should be enabled when strategy missing
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.C")


@responses.activate
def test_feature_unknown(unleash_client):
    """
    Unknown feature toggle should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Unknown")


@responses.activate
def test_feature_all_context_values(unleash_client):
    """
    Should allow all context values
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    context_values = {
        "userId": "123",
        "sessionId": "asd123",
        "remoteAddress": "127.0.0.1",
        "properties": {
            "customName": "customValue",
            "anotherName": "anotherValue"
        }
    }

    unleash_client.initialize_client()
    assert unleash_client.is_enabled("Feature.A", context_values)
