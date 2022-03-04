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
          "name": "F8.semverEQ",
          "description": "semver",
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
                  ]
              }
          ]
      },
      {
          "name": "F8.semverGT",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_GT",
                          "value": "1.2.2"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F8.semverLT",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_LT",
                          "value": "1.2.2"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F8.semverAlphaGT",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_GT",
                          "value": "2.0.0-alpha.1"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F8.semverAlphaLT",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_LT",
                          "value": "2.0.0-alpha.1"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F8.semverAlphaVersioning",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_LT",
                          "value": "2.0.0-alpha.3"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F8.alphaUnnumbered",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_GT",
                          "value": "2.0.0-alpha"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F8.releaseCandidate",
          "description": "semver",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "version",
                          "operator": "SEMVER_GT",
                          "value": "2.0.0-rc"
                      }
                  ]
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
def test_feature_constraintoperators_semvereq_enabled(unleash_client):
    """
    F8.semverEQ should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverEQ", {'version': '1.2.2'})


@responses.activate
def test_feature_constraintoperators_semvereq_disabled(unleash_client):
    """
    F8.semverEQ should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.semverEQ", {'version': '1.2.0'})


@responses.activate
def test_feature_constraintoperators_semvergt_enabled(unleash_client):
    """
    F8.semverGT should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverGT", {'version': '1.2.3'})


@responses.activate
def test_feature_constraintoperators_semvergt_disabled(unleash_client):
    """
    F8.semverGT should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.semverGT", {'version': '1.2.0'})


@responses.activate
def test_feature_constraintoperators_semverlt_enabled(unleash_client):
    """
    F8.semverLT should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverLT", {'version': '1.2.1'})


@responses.activate
def test_feature_constraintoperators_semverlt_disabled(unleash_client):
    """
    F8.semverLT should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.semverLT", {'version': '1.2.3'})


@responses.activate
def test_feature_constraintoperators_semveralphagt_beta(unleash_client):
    """
    F8.semverAlphaGT is less than beta
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverAlphaGT", {'version': '2.0.0-beta.1'})


@responses.activate
def test_feature_constraintoperators_semveralphagt_release(unleash_client):
    """
    F8.semverAlphaGT is less than release
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverAlphaGT", {'version': '2.0.0'})


@responses.activate
def test_feature_constraintoperators_semveralphalt_beta(unleash_client):
    """
    F8.semverAlphaLT is less than beta
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.semverAlphaLT", {'version': '2.0.0-beta.1'})


@responses.activate
def test_feature_constraintoperators_semveralphalt_oldbeta(unleash_client):
    """
    F8.semverAlphaLT is greater than old beta
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverAlphaLT", {'version': '1.9.1-beta.1'})


@responses.activate
def test_feature_constraintoperators_semveralphalt_release(unleash_client):
    """
    F8.semverAlpha is less than release
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.semverAlphaLT", {'version': '2.0.0'})


@responses.activate
def test_feature_constraintoperators_semveralphalt_alphas_lt(unleash_client):
    """
    F8.semverAlphaVersioning alpha.1 is less than alpha.3
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.semverAlphaVersioning", {'version': '2.0.0-alpha.1'})


@responses.activate
def test_feature_constraintoperators_semveralphalt_dif_alphas_gt(unleash_client):
    """
    F8.semverAlphaVersioning alpha.4 is greater than alpha.3
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.semverAlphaVersioning", {'version': '2.0.0-alpha.4'})


@responses.activate
def test_feature_constraintoperators_semverunnumbered_lt(unleash_client):
    """
    "F8.alphaUnnumbered - unnumbered is LT than numbered
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F8.alphaUnnumbered", {'version': '2.0.0-alpha.1'})


def test_feature_constraintoperators_semverrc_alpha(unleash_client):
    """
    F8.releaseCandidate - alpha is not greater than rc
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.releaseCandidate", {'version': '2.0.0-alpha.1'})

def test_feature_constraintoperators_semverc_beta(unleash_client):
    """
    F8.releaseCandidate - beta is not greater tha rc
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.releaseCandidate", {'version': '2.0.0-beta.1'})


def test_feature_constraintoperators_semverc_release(unleash_client):
    """
    F8.releaseCandidate - release is greater than rc
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F8.releaseCandidate", {'version': '2.0.0'})
