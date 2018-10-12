import responses
from tests.utilities.mocks.mock_features import MOCK_FEATURE_RESPONSE
from tests.utilities.testing_constants import URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS
from UnleashClient.constants import FEATURES_URL
from UnleashClient.api import get_feature_toggles


FULL_FEATURE_URL = URL + FEATURES_URL


@responses.activate
def test_get_feature_toggle_success():
    responses.add(responses.GET, FULL_FEATURE_URL, json=MOCK_FEATURE_RESPONSE, status=200)

    result = get_feature_toggles(URL,
                                 APP_NAME,
                                 INSTANCE_ID,
                                 CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert result["version"] == 1


@responses.activate
def test_get_feature_toggle_failure():
    responses.add(responses.GET, FULL_FEATURE_URL, json={}, status=500)

    result = get_feature_toggles(URL,
                                 APP_NAME,
                                 INSTANCE_ID,
                                 CUSTOM_HEADERS)

    assert len(responses.calls) == 1
    assert not result
