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
        url="https://gitlab.com/api/v4/feature_flags/unleash/32635317",
        app_name="pyIvan",
        instance_id="Sc5fv9aCyFPB4XcEFk-E",
        disable_metrics=True,
        disable_registration=True,
    )

    await my_client.initialize_client()

    while True:
        await asyncio.sleep(10)
        print(my_client.is_enabled("test"))


asyncio.run(main())
