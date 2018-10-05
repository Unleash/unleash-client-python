import responses
from requests import ConnectionError
from tests.unit.testing_constants import URL, APP_NAME, INSTANCE_ID, METRICS_INTERVAL, CUSTOM_HEADERS
from UnleashClient.api.register import register_client


@responses.activate
def test_register_client_success():
    responses.add(responses.POST, URL + "/api/client/register", json={}, status=202)

    result = register_client(URL,
                             APP_NAME,
                             INSTANCE_ID,
                             METRICS_INTERVAL,
                             CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert result


@responses.activate
def test_register_client_failure():
    responses.add(responses.POST, URL, json={}, status=500)

    result = register_client(URL,
                             APP_NAME,
                             INSTANCE_ID,
                             METRICS_INTERVAL,
                             CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert not result


@responses.activate
def test_register_client_exception():
    responses.add(responses.POST,
                  URL,
                  body=ConnectionError("Test connection error."),
                  status=200)

    result = register_client(URL,
                             APP_NAME,
                             INSTANCE_ID,
                             METRICS_INTERVAL,
                             CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert not result
