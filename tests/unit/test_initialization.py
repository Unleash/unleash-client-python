from UnleashClient import UnleashClient
from tests.unit.testing_constants import URL, APP_NAME, INSTANCE_ID, REFRESH_INTERVAL, METRICS_INTERVAL, DISABLE_METRICS, CUSTOM_HEADERS


def test_UC_initialize_default():
    client = UnleashClient(URL, APP_NAME)
    assert client.unleash_url == URL
    assert client.unleash_app_name == APP_NAME
    assert client.unleash_metrics_interval == 60000


def test_UC_initialize_full():
    client = UnleashClient(URL,
                           APP_NAME,
                           INSTANCE_ID,
                           REFRESH_INTERVAL,
                           METRICS_INTERVAL,
                           DISABLE_METRICS,
                           CUSTOM_HEADERS)
    assert client.unleash_instance_id == INSTANCE_ID
    assert client.unleash_refresh_interval == REFRESH_INTERVAL
    assert client.unleash_metrics_interval == METRICS_INTERVAL
    assert client.unleash_disable_metrics == DISABLE_METRICS
    assert client.unleash_custom_headers == CUSTOM_HEADERS


def test_UC_type_violation():
    client = UnleashClient(URL, APP_NAME, refresh_interval="60")
    assert client.unleash_url == URL
    assert client.unleash_app_name == APP_NAME
    assert client.unleash_refresh_interval == "60"
