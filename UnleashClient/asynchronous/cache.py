import abc
import json
from pathlib import Path
from typing import Any, Optional

import aiofile
import niquests as requests

from ..constants import FEATURES_URL, REQUEST_TIMEOUT
from ..vendor.fcache import AsyncFileCache as _FileCache


class AsyncBaseCache(abc.ABC):
    """
    Abstract base class for caches used for UnleashClient.

    If implementing your own bootstrapping methods:

    - Add your custom bootstrap method.
    - You must set the `bootstrapped` attribute to True after configuration is set.
    """

    bootstrapped = False
    bootstrap_data: Optional[str] = None

    @abc.abstractmethod
    async def set(self, key: str, value: Any):
        pass

    @abc.abstractmethod
    async def mset(self, data: dict):
        pass

    @abc.abstractmethod
    async def get(self, key: str, default: Optional[Any] = None):
        pass

    @abc.abstractmethod
    def exists(self, key: str):
        pass

    @abc.abstractmethod
    def destroy(self):
        pass


class AsyncFileCache(AsyncBaseCache):
    """
    The default cache for UnleashClient.  Uses `fcache <https://pypi.org/project/fcache/>`_ behind the scenes.

    You can boostrap the FileCache with initial configuration to improve resiliency on startup.  To do so:

    - Create a new FileCache instance.
    - Bootstrap the FileCache.
    - Pass your FileCache instance to UnleashClient at initialization along with `boostrap=true`.

    You can bootstrap from a dictionary, a json file, or from a URL.  In all cases, configuration should match the Unleash `/api/client/features <https://docs.getunleash.io/api/client/features>`_ endpoint.

    Example:

    .. code-block:: python

        from pathlib import Path
        from UnleashClient.asynchronous.cache import AsyncFileCache
        from UnleashClient.asynchronous import AsyncUnleashClient

        async def main():
            my_cache = AsyncFileCache("HAMSTER_API")
            await my_cache.bootstrap_from_file(Path("/path/to/boostrap.json"))
            unleash_client = AsyncUnleashClient(
                "https://my.unleash.server.com",
                "HAMSTER_API",
                cache=my_cache
            )

    :param name: Name of cache.
    :param directory: Location to create cache.  If empty, will use filecache default.
    """

    def __init__(
        self,
        name: str,
        directory: Optional[str] = None,
        request_timeout: int = REQUEST_TIMEOUT,
    ):
        self._cache = _FileCache(name, app_cache_dir=directory)
        self.bootstrap_data: Optional[str] = None
        self.request_timeout = request_timeout

    async def bootstrap_from_dict(self, initial_config: dict) -> None:
        """
        Loads initial Unleash configuration from a dictionary.

        Note: Pre-seeded configuration will only be used if UnleashClient is initialized with `bootstrap=true`.

        :param initial_config: Dictionary that contains initial configuration.
        """
        self.bootstrap_data = json.dumps(initial_config)
        await self.set(FEATURES_URL, self.bootstrap_data)
        self.bootstrapped = True

    async def bootstrap_from_file(self, initial_config_file: Path) -> None:
        """
        Loads initial Unleash configuration from a file.

        Note: Pre-seeded configuration will only be used if UnleashClient is initialized with `bootstrap=true`.

        :param initial_configuration_file: Path to document containing initial configuration.  Must be JSON.
        """
        async with aiofile.async_open(
            initial_config_file, "r", encoding="utf8"
        ) as bootstrap_file:
            self.bootstrap_data = await bootstrap_file.read()
            await self.set(FEATURES_URL, self.bootstrap_data)
            self.bootstrapped = True

    async def bootstrap_from_url(
        self,
        initial_config_url: str,
        headers: Optional[dict] = None,
        request_timeout: Optional[int] = None,
    ) -> None:
        """
        Loads initial Unleash configuration from a url.

        Note: Pre-seeded configuration will only be used if UnleashClient is initialized with `bootstrap=true`.

        :param initial_configuration_url: Url that returns document containing initial configuration.  Must return JSON.
        :param headers: Headers to use when GETing the initial configuration URL.
        """
        timeout = request_timeout if request_timeout else self.request_timeout
        response = await requests.aget(
            initial_config_url, headers=headers, timeout=timeout
        )
        self.bootstrap_data = response.text
        await self.set(FEATURES_URL, self.bootstrap_data)
        self.bootstrapped = True

    async def set(self, key: str, value: Any):
        await self._cache.set(key, value)
        await self._cache.sync()

    async def mset(self, data: dict):
        for k, v in data.items():
            await self._cache.set(k, v)
        await self._cache.sync()

    async def get(self, key: str, default: Optional[Any] = None):
        return await self._cache.get(key, default)

    def exists(self, key: str):
        return key in self._cache

    def destroy(self):
        return self._cache.delete()
