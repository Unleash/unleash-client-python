import responses
from requests import ConnectionError
from UnleashClient.constants import REGISTER_URL
from UnleashClient.api import register_client
from tests.utilities.testing_constants import URL, APP_NAME, INSTANCE_ID, METRICS_INTERVAL, CUSTOM_HEADERS, DEFAULT_STRATEGY_MAPPING


FULL_REGISTER_URL = URL + REGISTER_URL


@responses.activate
def test_register_client_success():
    responses.add(responses.POST, FULL_REGISTER_URL, json={}, status=202)

    result = register_client(URL,
                             APP_NAME,
                             INSTANCE_ID,
                             METRICS_INTERVAL,
                             CUSTOM_HEADERS,
                             DEFAULT_STRATEGY_MAPPING)

    assert len(responses.calls) == 1
    assert result


@responses.activate
def test_register_client_failure():
    responses.add(responses.POST, FULL_REGISTER_URL, json={}, status=500)

    result = register_client(URL,
                             APP_NAME,
                             INSTANCE_ID,
                             METRICS_INTERVAL,
                             CUSTOM_HEADERS,
                             DEFAULT_STRATEGY_MAPPING)

    assert len(responses.calls) == 1
    assert not result


@responses.activate
def test_register_client_exception():
    responses.add(responses.POST, FULL_REGISTER_URL, body=ConnectionError("Test connection error."), status=200)

    result = register_client(URL,
                             APP_NAME,
                             INSTANCE_ID,
                             METRICS_INTERVAL,
                             CUSTOM_HEADERS,
                             DEFAULT_STRATEGY_MAPPING)

    assert len(responses.calls) == 1
    assert not result
