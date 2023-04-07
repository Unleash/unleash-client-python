****************************************
Custom Cache
****************************************

Implementing a custom cache
#######################################

- Create a custom cache object by sub-classing the BaseCache object.
- Overwrite all the methods from the base class.  You can also add custom bootstraping methods!

.. code-block:: python

    from UnleashClient.cache import BaseCache
    from fcache.cache import FileCache as _Filecache

    class FileCache(BaseCache):
        # This is specific for FileCache.  Depending on the cache you're using, this may look different!
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

- Initialize your custom cache object and pass it into Unleash using the `cache` argument.
