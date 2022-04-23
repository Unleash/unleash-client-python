import abc
import json
from pathlib import Path
from typing import Any, Dict, Optional

import requests
from fcache.cache import FileCache as _FileCache
from UnleashClient.constants import FEATURES_URL, ETAG


class BaseCache(abc.ABC):
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
    def __init__(self, name: str, directory: Optional[str] = None):
        self._cache = _FileCache(name, app_cache_dir=directory)

    def bootstrap_from_dict(self, initial_config: dict) -> None:
        self.set(FEATURES_URL, initial_config)
        self.set(ETAG, "")

    def bootstrap_from_file(self, initial_config_file: Path) -> None:
        with open(initial_config_file, "r",  encoding="utf8") as bootstrap_file:
            self.set(FEATURES_URL, json.loads(bootstrap_file.read()))
            self.set(ETAG, "")

    def bootstrap_from_url(self, initial_config_url: str, headers: Optional[dict] = None) -> None:
        response = requests.get(initial_config_url, headers=headers)
        self.set(FEATURES_URL, response.json())
        self.set(ETAG, "")

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
