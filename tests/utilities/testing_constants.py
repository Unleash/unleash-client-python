from UnleashClient.constants import FEATURES_URL
from UnleashClient.strategies import (
    ApplicationHostname,
    Default,
    FlexibleRollout,
    GradualRolloutRandom,
    GradualRolloutSessionId,
    GradualRolloutUserId,
    RemoteAddress,
    UserWithId,
)

# General configs
APP_NAME = "pytest"
ENVIRONMENT = "unit"
INSTANCE_ID = "123"
REFRESH_INTERVAL = 15
REFRESH_JITTER = None
METRICS_INTERVAL = 10
METRICS_JITTER = None
DISABLE_METRICS = True
DISABLE_REGISTRATION = True
CUSTOM_HEADERS = {"name": "My random header."}
CUSTOM_OPTIONS = {"verify": False}

# URLs
URL = "http://localhost:4242/api"
INTEGRATION_URL = "http://localhost:4242/api"
PROJECT_URL = f"{URL}{FEATURES_URL}?project=ivan"

# Constants
IP_LIST = (
    "69.208.0.0/29,70.208.1.1,2001:db8:1234::/48,2002:db8:1234:0000:0000:0000:0000:0001"
)
PROJECT_NAME = "ivan"
ETAG_VALUE = 'W/"730-v0ozrE11zfZK13j7rQ5PxkXfjYQ"'

# Mapping
DEFAULT_STRATEGY_MAPPING = {
    "applicationHostname": ApplicationHostname,
    "default": Default,
    "gradualRolloutRandom": GradualRolloutRandom,
    "gradualRolloutSessionId": GradualRolloutSessionId,
    "gradualRolloutUserId": GradualRolloutUserId,
    "remoteAddress": RemoteAddress,
    "userWithId": UserWithId,
    "flexibleRollout": FlexibleRollout,
}
