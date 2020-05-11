import responses
from pytest import mark, param
from tests.utilities.mocks.mock_features import MOCK_FEATURE_RESPONSE
from tests.utilities.testing_constants import URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS, CUSTOM_OPTIONS
from UnleashClient.constants import FEATURES_URL
from UnleashClient.api import get_feature_toggles


FULL_FEATURE_URL = URL + FEATURES_URL


@responses.activate
@mark.parametrize("response,status,expected", (
    param(MOCK_FEATURE_RESPONSE, 200, lambda result: result["version"] == 1, id="success"),
    param(MOCK_FEATURE_RESPONSE, 202, lambda result: not result, id="failure"),
    param({}, 500, lambda result: not result, id="failure"),
))
def test_get_feature_toggle(response, status, expected):
    responses.add(responses.GET, FULL_FEATURE_URL, json=response, status=status)

    result = get_feature_toggles(URL,
                                 APP_NAME,
                                 INSTANCE_ID,
                                 CUSTOM_HEADERS,
                                 CUSTOM_OPTIONS)

    assert len(responses.calls) == 1
    assert expected(result)
