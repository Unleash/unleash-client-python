import uuid
import json
import pytest
import responses
from UnleashClient import UnleashClient
from UnleashClient.constants import FEATURES_URL, METRICS_URL, REGISTER_URL
from tests.utilities.testing_constants import URL, APP_NAME


MOCK_JSON = """
{
  "version": 2,
  "features": [
    {
      "name": "F9.globalSegmentOn",
      "description": "With global segment referencing constraint in on state",
      "enabled": true,
      "strategies": [
        {
          "name": "default",
          "parameters": {},
          "segments": [1]
        }
      ]
    },
    {
      "name": "F9.globalSegmentOff",
      "description": "With global segment referencing constraint in off state",
      "enabled": true,
      "strategies": [
        {
          "name": "default",
          "parameters": {},
          "segments": [2]
        }
      ]
    },
    {
      "name": "F9.globalSegmentAndConstraint",
      "description": "With global segment and constraint both on",
      "enabled": true,
      "strategies": [
        {
          "name": "default",
          "parameters": {},
          "constraints": [
            {
              "contextName": "version",
              "operator": "SEMVER_EQ",
              "value": "1.2.2"
            }
          ],
          "segments": [1]
        }
      ]
    },
    {
      "name": "F9.withMissingSegment",
      "description": "With global segment that doesn't exist",
      "enabled": true,
      "strategies": [
        {
          "name": "default",
          "parameters": {},
          "constraints": [
            {
              "contextName": "version",
              "operator": "SEMVER_EQ",
              "value": "1.2.2"
            }
          ],
          "segments": [3]
        }
      ]
    },
    {
      "name": "F9.withSeveralConstraintsAndSegments",
      "description": "With several segments and constraints",
      "enabled": true,
      "strategies": [
        {
          "name": "default",
          "parameters": {},
          "constraints": [
            {
              "contextName": "customNumber",
              "operator": "NUM_LT",
              "value": "10"
            },
            {
              "contextName": "version",
              "operator": "SEMVER_LT",
              "value": "3.2.2"
            }
          ],
          "segments": [1, 4, 5]
        }
      ]
    }
  ],
  "segments": [
    {
      "id": 1,
      "constraints": [
        {
          "contextName": "version",
          "operator": "SEMVER_EQ",
          "value": "1.2.2"
        }
      ]
    },
    {
      "id": 2,
      "constraints": [
        {
          "contextName": "version",
          "operator": "SEMVER_EQ",
          "value": "3.1.4"
        }
      ]
    },
    {
      "id": 3,
      "constraints": [
        {
          "contextName": "version",
          "operator": "SEMVER_EQ",
          "value": "3.1.4"
        }
      ]
    },
    {
      "id": 4,
      "constraints": [
        {
          "contextName": "customName",
          "operator": "STR_CONTAINS",
          "values": ["Pi"]
        }
      ]
    },
    {
      "id": 5,
      "constraints": [
        {
          "contextName": "slicesLeft",
          "operator": "NUM_LTE",
          "value": "4"
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
def test_feature_globalSegmentOff_should_be_disabled(unleash_client):
    """
    F9.globalSegmentOff should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F9.globalSegmentOff", {'version': '1.2.2'})


@responses.activate
def test_feature_globalSegmentOn_should_be_enabled(unleash_client):
    """
    F9.globalSegmentOn should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F9.globalSegmentOn", {'version': '1.2.2'})


@responses.activate
def test_feature_globalSegmentAndConstraint_should_be_enabled(unleash_client):
    """
    F9.globalSegmentAndConstraint should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F9.globalSegmentAndConstraint", {'version': '1.2.2'})


@responses.activate
def test_feature_withMissingSegment_should_force_evaluation_to_false(unleash_client):
    """
    F9.withMissingSegment should force evaluation to false
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F9.withMissingSegment", {'version': '1.2.2'})


@responses.activate
def test_feature_withSeveralConstraintsAndSegments_should_be_enabled(unleash_client):
    """
    F9.withSeveralConstraintsAndSegments should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F9.withSeveralConstraintsAndSegments", {"version": "1.2.2",
                                                                                  "customNumber": "3.14",
                                                                                  "customName": "Pie",
                                                                                  "slicesLeft": "4"})
