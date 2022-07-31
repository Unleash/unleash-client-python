from UnleashClient.api import get_feature_toggles
from UnleashClient.loader import load_features
from UnleashClient.constants import FEATURES_URL, ETAG
from UnleashClient.utils import LOGGER
from UnleashClient.cache import BaseCache
import os

def fetch_and_load_features(url: str,
                            app_name: str,
                            instance_id: str,
                            custom_headers: dict,
                            custom_options: dict,
                            cache: BaseCache,
                            features: dict,
                            strategy_mapping: dict,
                            project: str = None) -> None:
    (feature_provisioning, etag) = get_feature_toggles(
        url,
        app_name,
        instance_id,
        custom_headers,
        custom_options,
        project,
        cache.get(ETAG)
    )

    if feature_provisioning:
        # if there is somethign in shared memory, take it from there?
        # write it to cache
        # here i will write to the shared memory


        # from multiprocessing import shared_memory
        # print(type(feature_provisioning))
        # shm = shared_memory.SharedMemory(name="shared_features", create=True, size=len(feature_provisioning))
        # shm.buf = feature_provisioning
        # print("Writing to memory")
        # print(shm.buf)

        from multiprocessing import Process, Manager

        manager = Manager()
        d = manager.dict()
        print("Get from manager before save")
        print(d)
        d['test'] = 'test'
        print("Get from manager after save")
        print(d)
        print("Get from manager after saveprocess id: " + str(os.getpid()) + "</p>")
        cache.set(FEATURES_URL, feature_provisioning)
    else:
        LOGGER.debug("No feature provisioning returned from server, using cached provisioning.")

    if etag:
        cache.set(ETAG, etag)

    load_features(cache, features, strategy_mapping)
