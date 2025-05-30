from typing import Optional

from yggdrasil_engine.engine import UnleashEngine

from ...api.asynchronous import async_get_feature_toggles
from ...asynchronous.cache import AsyncBaseCache
from ...asynchronous.loader import async_load_features
from ...constants import ETAG, FEATURES_URL
from ...utils import LOGGER


async def async_fetch_and_load_features(
    url: str,
    app_name: str,
    instance_id: str,
    headers: dict,
    custom_options: dict,
    cache: AsyncBaseCache,
    request_timeout: int,
    request_retries: int,
    engine: UnleashEngine,
    project: Optional[str] = None,
) -> None:
    (state, etag) = await async_get_feature_toggles(
        url,
        app_name,
        instance_id,
        headers,
        custom_options,
        request_timeout,
        request_retries,
        project,
        await cache.get(ETAG),
    )

    if state:
        await cache.set(FEATURES_URL, state)
    else:
        LOGGER.debug(
            "No feature provisioning returned from server, using cached provisioning."
        )

    if etag:
        await cache.set(ETAG, etag)

    await async_load_features(cache, engine)
