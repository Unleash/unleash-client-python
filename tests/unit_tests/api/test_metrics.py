import responses
from requests import ConnectionError
from tests.utilities.testing_constants import URL, CUSTOM_HEADERS
from tests.utilities.mocks.mock_metrics import MOCK_METRICS_REQUEST
from UnleashClient.constants import METRICS_URL
from UnleashClient.api import send_metrics


FULL_METRICS_URL = URL + METRICS_URL


@responses.activate
def test_send_metrics_success():
    responses.add(responses.POST, FULL_METRICS_URL, json={}, status=202)

    result = send_metrics(URL, MOCK_METRICS_REQUEST, CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert result


@responses.activate
def test_send_metrics_failure():
    responses.add(responses.POST, FULL_METRICS_URL, json={}, status=500)

    result = send_metrics(URL, MOCK_METRICS_REQUEST, CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert not result


@responses.activate
def test_register_client_exception():
    responses.add(responses.POST, FULL_METRICS_URL, body=ConnectionError("Test connection error."), status=200)

    result = send_metrics(URL, MOCK_METRICS_REQUEST, CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert not result
