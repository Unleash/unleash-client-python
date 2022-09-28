import abc
import json
from pathlib import Path
from typing import Any, Optional

import requests
from fcache.cache import FileCache as _FileCache
from UnleashClient.constants import FEATURES_URL, REQUEST_TIMEOUT


class BaseCache(abc.ABC):
    """
    Abstract base class for caches used for UnleashClient.

    If implementing your own bootstrapping methods, you must set the `bootstrapped` attribute to True after configuration is set.
    """
    bootstrapped = False

    @abc.abstractmethod
    def set(self, key: str, value: Any):
        pass

    @abc.abstractmethod
    def mset(self, data: dict):
        pass

    @abc.abstractmethod
    def get(self, key: str, default: Optional[Any] = None):
        pass

    @abc.abstractmethod
    def exists(self, key: str):
        pass

    @abc.abstractmethod
    def destroy(self):
        pass


class FileCache(BaseCache):
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
        from UnleashClient.cache import FileCache
        from UnleashClient import UnleashClient

        my_cache = FileCache("HAMSTER_API")
        my_cache.bootstrap_from_file(Path("/path/to/boostrap.json"))
        unleash_client = UnleashClient(
            "https://my.unleash.server.com",
            "HAMSTER_API",
            cache=cache
        )

    :param name: Name of cache.
    :param directory: Location to create cache.  If empty, will use filecache default.
    """
    def __init__(self, name: str, directory: Optional[str] = None):
        self._cache = _FileCache(name, app_cache_dir=directory)

    def bootstrap_from_dict(self, initial_config: dict) -> None:
        """
        Loads initial Unleash configuration from a dictionary.

        Note: Pre-seeded configuration will only be used if UnleashClient is initialized with `bootstrap=true`.

        :param initial_config: Dictionary that contains initial configuration.
        """
        self.set(FEATURES_URL, initial_config)
        self.bootstrapped = True

    def bootstrap_from_file(self, initial_config_file: Path) -> None:
        """
        Loads initial Unleash configuration from a file.

        Note: Pre-seeded configuration will only be used if UnleashClient is initialized with `bootstrap=true`.

        :param initial_configuration_file: Path to document containing initial configuration.  Must be JSON.
        """
        with open(initial_config_file, "r",  encoding="utf8") as bootstrap_file:
            self.set(FEATURES_URL, json.loads(bootstrap_file.read()))
            self.bootstrapped = True

    def bootstrap_from_url(self, initial_config_url: str, headers: Optional[dict] = None) -> None:
        """
        Loads initial Unleash configuration from a url.

        Note: Pre-seeded configuration will only be used if UnleashClient is initialized with `bootstrap=true`.

        :param initial_configuration_url: Url that returns document containing initial configuration.  Must return JSON.
        :param headers: Headers to use when GETing the initial configuration URL.
        """
        response = requests.get(initial_config_url, headers=headers, timeout=REQUEST_TIMEOUT)
        self.set(FEATURES_URL, response.json())
        self.bootstrapped = True

    def set(self, key: str, value: Any):
        self._cache[key] = value
        self._cache.sync()

    def mset(self, data: dict):
        self._cache.update(data)
        self._cache.sync()

    def get(self, key: str, default: Optional[Any] = None):
        return self._cache.get(key, default)

    def exists(self, key: str):
        return key in self._cache

    def destroy(self):
        return self._cache.delete()
