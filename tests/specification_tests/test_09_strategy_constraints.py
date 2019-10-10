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
         "name":"Feature.constraints.simple",
         "description":"Enabled only in dev",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               },
               "constraints":[
                  {
                     "contextName":"environment",
                     "operator":"IN",
                     "values":[
                        "dev"
                     ]
                  }
               ]
            }
         ]
      },
      {
         "name":"Feature.constraints.list",
         "description":"Enabled in dev, stage, prod",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               },
               "constraints":[
                  {
                     "contextName":"environment",
                     "operator":"IN",
                     "values":[
                        "dev",
                        "stage",
                        "prod"
                     ]
                  }
               ]
            }
         ]
      },
      {
         "name":"Feature.constraints.multi",
         "description":"Enabled in prod and only for users 1, 2, 3",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               },
               "constraints":[
                  {
                     "contextName":"environment",
                     "operator":"IN",
                     "values":[
                        "prod"
                     ]
                  },
                  {
                     "contextName":"userId",
                     "operator":"IN",
                     "values":[
                        "1",
                        "2",
                        "3"
                     ]
                  },
                  {
                     "contextName":"appName",
                     "operator":"NOT_IN",
                     "values":[
                        "web",
                        "sun-app"
                     ]
                  }
               ]
            }
         ]
      },
      {
         "name":"Feature.constraints.custom",
         "description":"Enabled in prod in country IN (norway or sweeden)",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               },
               "constraints":[
                  {
                     "contextName":"environment",
                     "operator":"IN",
                     "values":[
                        "prod"
                     ]
                  },
                  {
                     "contextName":"country",
                     "operator":"IN",
                     "values":[
                        "norway",
                        "sweeden"
                     ]
                  }
               ]
            }
         ]
      },
      {
         "name":"Feature.constraints.dual",
         "description":"Enabled in prod and not in qa and dev",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               },
               "constraints":[
                  {
                     "contextName":"environment",
                     "operator":"IN",
                     "values":[
                        "prod",
                        "dev"
                     ]
                  },
                  {
                     "contextName":"environment",
                     "operator":"NOT_IN",
                     "values":[
                        "dev",
                        "qa"
                     ]
                  }
               ]
            }
         ]
      },
      {
         "name":"Feature.constraints.empty",
         "description":"Always disabled for empty list of values",
         "enabled":true,
         "strategies":[
            {
               "name":"default",
               "parameters":{

               },
               "constraints":[
                  {
                     "contextName":"environment",
                     "operator":"IN",
                     "values":[

                     ]
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
def test_feature_simple_defaultenv(unleash_client):
    """
    Feature.constraints.simple should not be enabled in default environment.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("Feature.constraints.simple", {})


@responses.activate
def test_feature_constraintssimple_devenv(unleash_client):
    """
    Feature.constraints.simple should be enabled in dev environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "dev"
    assert unleash_client.is_enabled("Feature.constraints.simple", {})


@responses.activate
def test_feature_constraintslist_stageenv(unleash_client):
    """
    Feature.constraints.list should be enabled in stage environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "stage"
    assert unleash_client.is_enabled("Feature.constraints.list", {})


@responses.activate
def test_feature_constraintslist_qaenv(unleash_client):
    """
    Feature.constraints.list should NOT be enabled in qa environment
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "qa"
    assert not unleash_client.is_enabled("Feature.constraints.list", {})


@responses.activate
def test_feature_constraintsmulti_user2(unleash_client):
    """
    Feature.constraints.multi should be enabled in prod for user 2
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "prod"
    assert unleash_client.is_enabled("Feature.constraints.multi", {"userId": "2"})


@responses.activate
def test_feature_constraintsmulti_unknownuser(unleash_client):
    """
    Feature.constraints.multi should NOT be enabled for unknown user
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "prod"
    assert not unleash_client.is_enabled("Feature.constraints.multi", {})


@responses.activate
def test_feature_constraintsmulti_web(unleash_client):
    """
    Feature.constraints.multi should NOT be enabled appName=web
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "prod"
    unleash_client.unleash_static_context["appName"] = "web"
    assert not unleash_client.is_enabled("Feature.constraints.multi", {"userId": "2"})


@responses.activate
def test_feature_constraintscustom_norway(unleash_client):
    """
    Feature.constraints.custom should be enabled in prod for norway.
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "prod"
    unleash_client.unleash_static_context["appName"] = "web"
    assert unleash_client.is_enabled("Feature.constraints.custom", {"properties": {"country": "norway"}})


@responses.activate
def test_feature_constraintscustom_denmark(unleash_client):
    """
    Feature.constraints.custom should NOT be enabled in prod for denmark
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "prod"
    unleash_client.unleash_static_context["appName"] = "web"
    assert not unleash_client.is_enabled("Feature.constraints.custom", {"properties": {"country": "denmark"}})


@responses.activate
def test_feature_constraintsdual_prod(unleash_client):
    """
    Feature.constraints.dual should be enabled in prod
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "prod"
    assert unleash_client.is_enabled("Feature.constraints.dual", {})


@responses.activate
def test_feature_constraintsdual_dev(unleash_client):
    """
    Feature.constraints.dual should not be enabled in dev
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "dev"
    assert not unleash_client.is_enabled("Feature.constraints.dual", {})


@responses.activate
def test_feature_constraintsempty(unleash_client):
    """
    Feature.constraints.empty should always be disabled
    """
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(responses.GET, URL + FEATURES_URL, json=json.loads(MOCK_JSON), status=200)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Tests
    unleash_client.initialize_client()
    unleash_client.unleash_static_context["environment"] = "dev"
    assert not unleash_client.is_enabled("Feature.constraints.empty", {})
