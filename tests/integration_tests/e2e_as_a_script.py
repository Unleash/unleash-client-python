import time
import random
from UnleashClient import UnleashClient

my_unleash_client = UnleashClient("http://localhost:4242", "fake_app")
my_unleash_client.initialize_client()
time.sleep(10)

for _ in range(60):
    email = random.choice(["meep@meep.com", "miss@miss.com"])
    time.sleep(5)
    my_unleash_client.is_enabled("UserWithId", context={"userId": email})

my_unleash_client.destroy()
