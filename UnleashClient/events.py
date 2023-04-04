from typing import Optional
from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class UnleashEventType(Enum):
    FEATURE_FLAG = "feature_flag"
    VARIANT = "variant"


@dataclass
class UnleashEvent:
    event_type: UnleashEventType
    event_id: UUID
    context: dict
    enabled: bool
    feature_name: str
    variant: Optional[str] = ''
