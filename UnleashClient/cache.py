import abc

from fcache.cache import FileCache as _FileCache


class BaseCache(abc.ABC):
    @abc.abstractmethod
    def set(self, key, value):
        pass

    @abc.abstractmethod
    def mset(self, data):
        pass

    @abc.abstractmethod
    def get(self, key, default=None):
        pass

    @abc.abstractmethod
    def exists(self, key):
        pass

    @abc.abstractmethod
    def destroy(self):
        pass


class FileCache(BaseCache):
    def __init__(self, name, directory=None):
        self._cache = _FileCache(name, app_cache_dir=directory)

    def set(self, key, value):
        self._cache[key] = value
        self._cache.sync()

    def mset(self, data):
        self._cache.update(data)
        self._cache.sync()

    def get(self, key, default=None):
        return self._cache.get(key, default)

    def exists(self, key):
        return key in self._cache

    def destroy(self):
        return self._cache.delete()
