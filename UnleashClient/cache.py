import abc
from typing import Any, Optional

from fcache.cache import FileCache as _FileCache


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
