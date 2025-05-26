# ---
import asyncio
import logging
import sys

from UnleashClient.asynchronous import AsyncUnleashClient

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)
# ---


async def main():
    my_client = AsyncUnleashClient(
        url="https://unleash.herokuapp.com/api",
        environment="staging",
        app_name="pyIvan",
    )

    await my_client.initialize_client()

    while True:
        await asyncio.sleep(10)
        context = {"userId": "1", "sound": "woof"}
        print(f"ivantest: {my_client.is_enabled('ivantest', context)}")


asyncio.run(main())
