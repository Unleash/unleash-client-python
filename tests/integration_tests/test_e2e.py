from UnleashClient.api import register_client
from UnleashClient.api import get_feature_toggles
from tests.utilities.testing_constants import INTEGRATION_URL, APP_NAME, INSTANCE_ID, METRICS_INTERVAL, CUSTOM_HEADERS


def test_e2e_temp():
    register_client(INTEGRATION_URL,
                    APP_NAME,
                    INSTANCE_ID,
                    METRICS_INTERVAL,
                    CUSTOM_HEADERS)

    features = get_feature_toggles(INTEGRATION_URL, APP_NAME, INSTANCE_ID, CUSTOM_HEADERS)

    assert features
