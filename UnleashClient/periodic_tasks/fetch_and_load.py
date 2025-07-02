from typing import Optional
import uuid

from yggdrasil_engine.engine import UnleashEngine

from UnleashClient.api import get_feature_toggles
from UnleashClient.cache import BaseCache
from UnleashClient.constants import ETAG, FEATURES_URL
from UnleashClient.events import UnleashEventType, UnleashFetchedEvent
from UnleashClient.loader import load_features
from UnleashClient.utils import LOGGER


def fetch_and_load_features(
    url: str,
    app_name: str,
    instance_id: str,
    headers: dict,
    custom_options: dict,
    cache: BaseCache,
    request_timeout: int,
    request_retries: int,
    engine: UnleashEngine,
    project: Optional[str] = None,
    event_callback: Optional[callable] = None,
) -> None:
    (state, etag) = get_feature_toggles(
        url,
        app_name,
        instance_id,
        headers,
        custom_options,
        request_timeout,
        request_retries,
        project,
        cache.get(ETAG),
    )

    if state:
        cache.set(FEATURES_URL, state)
        if event_callback:
            event = UnleashFetchedEvent(
                event_type=UnleashEventType.FETCHED,
                event_id=uuid.uuid4(),
                raw_features=state,
            )
            event_callback(event)
    else:
        LOGGER.debug(
            "No feature provisioning returned from server, using cached provisioning."
        )

    if etag:
        cache.set(ETAG, etag)

    load_features(cache, engine)
