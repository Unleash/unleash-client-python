import time
import pytest
import responses
from UnleashClient import UnleashClient


@pytest.fixture()
def unleash_client():
    unleash_client = UnleashClient("http://localhost:4242/api", "unleash-python-integration")
    yield unleash_client
    unleash_client.destroy()


def test_uc_is_enabled(unleash_client):
    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    for x in range(100):
        assert unleash_client.is_enabled("Demo")
        time.sleep(15)
