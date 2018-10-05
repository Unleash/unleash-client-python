from UnleashClient.api.register import register_client
from UnleashClient.api.features import get_feature_toggles
from tests.integration.testing_constants import URL, APP_NAME, INSTANCE_ID, METRICS_INTERVAL, CUSTOM_HEADERS


def test_e2e_temp():
    register_client(URL,
                    APP_NAME,
                    INSTANCE_ID,
                    METRICS_INTERVAL,
                    CUSTOM_HEADERS)

    features = get_feature_toggles(URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS)

    assert features
