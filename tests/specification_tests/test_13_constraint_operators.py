import uuid
from datetime import datetime
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
          "name": "F1.startsWith",
          "description": "startsWith",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "customField",
                          "operator": "STR_STARTS_WITH",
                          "values": ["some-string"]

                      }
                  ]
              }
          ]
      },
      {
          "name": "F2.startsWith.multiple",
          "description": "endsWith",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "customField",
                          "operator": "STR_STARTS_WITH",
                          "values": ["e1", "e2"]

                      }
                  ]
              }
          ]
      },
      {
          "name": "F3.endsWith",
          "description": "endsWith",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "email",
                          "operator": "STR_ENDS_WITH",
                          "values": ["@some-email.com"]
                      }
                  ]
              }
          ]
      },
      {
          "name": "F3.endsWith.ignoringCase",
          "description": "endsWith",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "email",
                          "operator": "STR_ENDS_WITH",
                          "values": ["@some-email.com"],
                          "caseInsensitive": true
                      }
                  ]
              }
          ]
      },
      {
          "name": "F4.contains",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "email",
                          "operator": "STR_CONTAINS",
                          "values": ["email"]

                      }
                  ]
              }
          ]
      },
      {
          "name": "F4.contains.inverted",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "email",
                          "operator": "STR_CONTAINS",
                          "values": ["email"],
                          "inverted": true

                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numEq",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_EQ",
                          "value": "12"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numEq.float",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_EQ",
                          "value": "12.0"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numEq.inverted",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_EQ",
                          "value": "12",
                          "inverted": true
                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numGT",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_GT",
                          "value": "12"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numGTE",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_GTE",
                          "value": "12"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numLT",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_LT",
                          "value": "12"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F5.numLTE",
          "description": "contains",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_LTE",
                          "value": "12"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F6.number-range",
          "description": "range of numbers",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "someValue",
                          "operator": "NUM_GT",
                          "value": "12"
                      },
                      {
                          "contextName": "someValue",
                          "operator": "NUM_LT",
                          "value": "16"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F7.dateAfter",
          "description": "dates",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "currentTime",
                          "operator": "DATE_AFTER",
                          "value": "2022-01-29T13:00:00.000Z"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F7.dateBefore",
          "description": "dates",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "currentTime",
                          "operator": "DATE_BEFORE",
                          "value": "2022-01-29T13:00:00.000Z"
                      }
                  ]
              }
          ]
      },
      {
          "name": "F7.date-range",
          "description": "dates",
          "enabled": true,
          "strategies": [
              {
                  "name": "default",
                  "parameters": {},
                  "constraints": [
                      {
                          "contextName": "currentTime",
                          "operator": "DATE_AFTER",
                          "value": "2022-01-22T13:00:00.000Z"
                      },
                      {
                          "contextName": "currentTime",
                          "operator": "DATE_BEFORE",
                          "value": "2022-01-29T13:00:00.000Z"
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
def test_feature_constraintoperators_startswith_enabled(unleash_client):
    """
    F1.startsWith should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F1.startsWith", {'customField': 'some-string-is-cool'})


@responses.activate
def test_feature_constraintoperators_startswith_disabled(unleash_client):
    """
    F1.startsWith should be disabled"
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F1.startsWith", {'customField': 'some2-string-is-cool'})


@responses.activate
def test_feature_constraintoperators_startswith_enabled_multiple(unleash_client):
    """
    F2.startsWith.multiple should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F2.startsWith.multiple", {'customField': 'e2 cool'})


@responses.activate
def test_feature_constraintoperators_startswith_disabled_multiple(unleash_client):
    """
    F2.startsWith.multiple should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F2.startsWith.multiple", {'customField': 'cool e2'})


@responses.activate
def test_feature_constraintoperators_endswith_enabled(unleash_client):
    """
    F3.endsWith should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F3.endsWith", {'email': '@some-email.com'})


@responses.activate
def test_feature_constraintoperators_endswith_incorrectcasing(unleash_client):
    """
    F3.endsWith should be disabled when casing is incorrect
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F3.endsWith", {'email': '@some-EMAIL.com'})


@responses.activate
def test_feature_constraintoperators_endswith_ignorecasing(unleash_client):
    """
    F3.endsWith should be disabled when casing is incorrect
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F3.endsWith.ignoringCase", {'email': '@SOME-EMAIL.com'})


@responses.activate
def test_feature_constraintoperators_endswith_disabled(unleash_client):
    """
    F3.endsWith should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F3.endsWith", {'email': '@another-email.com'})


@responses.activate
def test_feature_constraintoperators_contains_enabled(unleash_client):
    """
    F4.contains should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F4.contains", {'email': '@some-email.com'})


@responses.activate
def test_feature_constraintoperators_contains_disabled(unleash_client):
    """
    F4.contains should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F4.contains", {'email': '@another.com'})


@responses.activate
def test_feature_constraintoperators_contains_inverted(unleash_client):
    """
    F4.contains.inverted should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F4.contains.inverted", {'email': '@another.com'})


@responses.activate
def test_feature_constraintoperators_numeq_enabled(unleash_client):
    """
    F5.numEq
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numEq", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numeq_enabled_floats(unleash_client):
    """
    F5.numEq works for floats
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numEq", {'someValue': 12.0})


@responses.activate
def test_feature_constraintoperators_numeq_inverted(unleash_client):
    """
    F5.numEq.inverted should be true
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F5.numEq.inverted", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numeqfloat_enabled_floats(unleash_client):
    """
    F5.numEq.float works for floats
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numEq.float", {'someValue': 12.0})


@responses.activate
def test_feature_constraintoperators_numeqfloat_enabled_int(unleash_client):
    """
    F5.numEq.float works for integers
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numEq.float", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numgt_enabled(unleash_client):
    """
    F5.numGT should be true
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numGT", {'someValue': 13})


@responses.activate
def test_feature_constraintoperators_numgt_disabled(unleash_client):
    """
    F5.numGT should be false
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F5.numGT", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numgte_enabled_equal(unleash_client):
    """
    F5.numGTE should be true when equal
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numGTE", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numgte_enabled_greater(unleash_client):
    """
    F5.numGTE should be true when larger
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numGTE", {'someValue': 13})


@responses.activate
def test_feature_constraintoperators_numgte_disabled(unleash_client):
    """
    F5.numGTE should be false when lower
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F5.numGTE", {'someValue': 11})


@responses.activate
def test_feature_constraintoperators_numlte_enabled_equal(unleash_client):
    """
    F5.numLTE should be true when equal
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numLTE", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numlte_enabled_less(unleash_client):
    """
    F5.numLTE should be true when lower
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numLTE", {'someValue': 0})


@responses.activate
def test_feature_constraintoperators_numlt_enabled_less(unleash_client):
    """
    F5.numLT should be true when lower
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F5.numLT", {'someValue': 0})


@responses.activate
def test_feature_constraintoperators_numlt_disabled_equal(unleash_client):
    """
    F5.numLT should be false when equal
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F5.numLT", {'someValue': 12})


@responses.activate
def test_feature_constraintoperators_numberranger_disabled(unleash_client):
    """
    F6.number-range should be false when not in range
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F6.number-range", {'someValue': 11})


@responses.activate
def test_feature_constraintoperators_numberranger_enabled(unleash_client):
    """
    F6.number-range should be true when in range
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F6.number-range", {'someValue': 14})


@responses.activate
def test_feature_constraintoperators_dateafter_enabled(unleash_client):
    """
    F7.dateAfter should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F7.dateAfter", {'currentTime': datetime(2022, 1, 30, 13)})


@responses.activate
def test_feature_constraintoperators_dateafter_disabled(unleash_client):
    """
    F7.dateAfter should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F7.dateAfter", {'currentTime': datetime(2022, 1, 28, 13)})


@responses.activate
def test_feature_constraintoperators_dateafter_exclusive(unleash_client):
    """
    F7.dateAfter should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F7.dateAfter", {'currentTime': datetime(2022, 1, 29, 13)})


@responses.activate
def test_feature_constraintoperators_datebefore_enabled(unleash_client):
    """
    F7.dateBefore should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F7.dateBefore", {'currentTime': datetime(2022, 1, 28, 13)})


@responses.activate
def test_feature_constraintoperators_datebefore_disabled(unleash_client):
    """
    F7.dateBefore should be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("F7.dateBefore", {'currentTime': datetime(2022, 1, 30, 13)})


@responses.activate
def test_feature_constraintoperators_daterange(unleash_client):
    """
    "F7.data-range should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert unleash_client.is_enabled("F7.date-range", {'currentTime': datetime(2022, 1, 25, 13)})
  