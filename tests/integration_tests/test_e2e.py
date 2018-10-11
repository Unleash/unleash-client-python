import time
import random
import pytest
from UnleashClient import UnleashClient
from tests.utilities.testing_constants import INTEGRATION_URL, APP_NAME


@pytest.fixture()
def unleash_client():
    my_unleash_client = UnleashClient(INTEGRATION_URL, APP_NAME)
    yield my_unleash_client
    my_unleash_client.destroy()


def test_e2e(unleash_client):
    my_unleash_client = unleash_client
    my_unleash_client.initialize_client()

    time.sleep(10)
    for _ in range(60):
        email = random.choice(["meep@meep.com", "miss@miss.com"])
        time.sleep(5)
        my_unleash_client.is_enabled("UserWithId", context={"userId": email})
