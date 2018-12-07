from UnleashClient.strategies import ApplicationHostname, Default, GradualRolloutRandom, \
    GradualRolloutSessionId, GradualRolloutUserId, UserWithId, RemoteAddress

# General configs
APP_NAME = "pytest"
INSTANCE_ID = "123"
REFRESH_INTERVAL = 15
METRICS_INTERVAL = 10
DISABLE_METRICS = True
CUSTOM_HEADERS = {"name": "My random header."}

# URLs
URL = "http://localhost:4242/api"
INTEGRATION_URL = "http://localhost:4242/api"

# Constants
IP_LIST = "69.208.0.0/29,70.208.1.1,2001:db8:1234::/48,2002:db8:1234:0000:0000:0000:0000:0001"

# Mapping
DEFAULT_STRATEGY_MAPPING = {
    "applicationHostname": ApplicationHostname,
    "default": Default,
    "gradualRolloutRandom": GradualRolloutRandom,
    "gradualRolloutSessionId": GradualRolloutSessionId,
    "gradualRolloutUserId": GradualRolloutUserId,
    "remoteAddress": RemoteAddress,
    "userWithId": UserWithId
}
