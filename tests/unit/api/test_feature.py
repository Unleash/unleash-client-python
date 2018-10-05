import responses
from tests.unit.unleash_mocks import MOCK_FEATURE_RESPONSE
from tests.unit.testing_constants import URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS
from UnleashClient.api.features import get_feature_toggles


@responses.activate
def test_register_client_success():
    responses.add(responses.GET, URL + "/api/client/features", json=MOCK_FEATURE_RESPONSE, status=200)

    result = get_feature_toggles(URL,
                                 APP_NAME,
                                 INSTANCE_ID,
                                 CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert result["version"] == 1


@responses.activate
def test_register_client_failure():
    responses.add(responses.POST, URL, json={}, status=500)

    result = get_feature_toggles(URL,
                                 APP_NAME,
                                 INSTANCE_ID,
                                 CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert not result
