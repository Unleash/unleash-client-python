import uuid
import json
import pytest
import responses
from UnleashClient import UnleashClient
from UnleashClient.constants import FEATURES_URL, METRICS_URL, REGISTER_URL
from tests.utilities.testing_constants import URL, APP_NAME


MOCK_JSON = """
{
   "version":1,
   "features":[
      {
         "name":"Feature.Variants.A",
         "description":"Enabled",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{}
            }
         ],
         "variants":[
            {
               "name":"variant1",
               "weight":1,
               "payload":{
                  "type":"string",
                  "value":"val1"
               }
            }
         ]
      },
      {
         "name":"Feature.Variants.B",
         "description":"Enabled for user=123",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{}
            }
         ],
         "variants":[
            {
               "name":"variant1",
               "weight":1,
               "payload":{
                  "type":"string",
                  "value":"val1"
               }
            },
            {
               "name":"variant2",
               "weight":1,
               "payload":{
                  "type":"string",
                  "value":"val2"
               }
            }
         ]
      },
      {
         "name":"Feature.Variants.C",
         "description":"Testing three variants",
         "enabled":true,
         "strategies":[

         ],
         "variants":[
            {
               "name":"variant1",
               "weight":33,
               "payload":{
                  "type":"string",
                  "value":"val1"
               }
            },
            {
               "name":"variant2",
               "weight":33,
               "payload":{
                  "type":"string",
                  "value":"val2"
               }
            },
            {
               "name":"variant3",
               "weight":33,
               "payload":{
                  "type":"string",
                  "value":"val3"
               }
            }
         ]
      },
      {
         "name":"Feature.Variants.D",
         "description":"Variants with payload",
         "enabled":true,
         "strategies":[

         ],
         "variants":[
            {
               "name":"variant1",
               "weight":1,
               "payload":{
                  "type":"string",
                  "value":"val1"
               }
            },
            {
               "name":"variant2",
               "weight":49,
               "payload":{
                  "type":"string",
                  "value":"val2"
               }
            },
            {
               "name":"variant3",
               "weight":50,
               "payload":{
                  "type":"string",
                  "value":"val3"
               }
            }
         ]
      },
      {
         "name":"Feature.Variants.override.D",
         "description":"Variant with overrides",
         "enabled":true,
         "strategies":[

         ],
         "variants":[
            {
               "name":"variant1",
               "weight":33,
               "payload":{
                  "type":"string",
                  "value":"val1"
               },
               "overrides":[
                  {
                     "contextName":"userId",
                     "values":[
                        "132",
                        "61"
                     ]
                  }
               ]
            },
            {
               "name":"variant2",
               "weight":33,
               "payload":{
                  "type":"string",
                  "value":"val2"
               }
            },
            {
               "name":"variant3",
               "weight":34,
               "payload":{
                  "type":"string",
                  "value":"val3"
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
def test_feature_variantsA_enabled(unleash_client):
    """
    Feature.Variants.A should be enabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'userId': "0"
    }

    expected_result = {
        "name": "variant1",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    assert unleash_client.select_variant("Feature.Variants.A", context) == expected_result


@responses.activate
def test_feature_variantsMissingToggle(unleash_client):
    """
    Feature.Variants.MissingToggle should be disabled missing toggle
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {}

    expected_result = {
        "name": "disabled",
        "enabled": False
    }

    assert unleash_client.select_variant("Feature.Variants.MissingToggle", context) == expected_result


@responses.activate
def test_feature_variantsB_enabled(unleash_client):
    """
    Feature.Variants.B should be enabled for user 2
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    context = {
        'userId': "2"
    }

    expected_result = {
        "name": "variant1",
        "payload": {
            "type": "string",
            "value": "val1"
        },
        "enabled": True
    }

    assert unleash_client.select_variant("Feature.Variants.B", context) == expected_result
