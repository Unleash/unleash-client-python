import time
from UnleashClient import UnleashClient

# ---
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
# ---

my_client = UnleashClient(
    url="https://eu.unleash-hosted.com/demo/api",
    environment="staging",
    app_name="pyIvan",
    custom_headers={'Authorization': '56907a2fa53c1d16101d509a10b78e36190b0f918d9f122d'}
)

my_client.initialize_client()

while True:
    time.sleep(10)
    context = {
        'userId': "1"
    }
    print(my_client.is_enabled("ivantest", context))
