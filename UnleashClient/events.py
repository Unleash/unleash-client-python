from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import UUID


class UnleashEventType(Enum):
    """
    Indicates what kind of event was triggered.
    """

    FEATURE_FLAG = "feature_flag"
    VARIANT = "variant"


@dataclass
class UnleashEvent:
    """
    Dataclass capturing information from an Unleash feature flag or variant check.
    """

    event_type: UnleashEventType
    event_id: UUID
    context: dict
    enabled: bool
    feature_name: str
    variant: Optional[str] = ""
