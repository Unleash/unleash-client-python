# Library
SDK_NAME = "unleash-client-python"
SDK_VERSION = "0.1.1"
REQUEST_TIMEOUT = 30

# =Unleash=
DEFAULT_STRATEGIES = ["default",
                      "userWithId",
                      "gradualRolloutUserId",
                      "gradualRolloutSessionId",
                      "gradualRolloutRandom",
                      "remoteAddress",
                      "applicationHostname"]

APPLICATION_HEADERS = {"Content-Type": "application/json"}

# Paths
REGISTER_URL = "/api/client/register"
FEATURES_URL = "/api/client/features"
METRICS_URL = "/api/client/metrics"
