from importlib_metadata import version

# Library
SDK_NAME = "unleash-client-python"
SDK_VERSION = version("UnleashClient")
REQUEST_TIMEOUT = 30
METRIC_LAST_SENT_TIME = "mlst"

# =Unleash=
APPLICATION_HEADERS = {"Content-Type": "application/json"}
DISABLED_VARIATION = {
    'name': 'disabled',
    'enabled': False
}

# Paths
REGISTER_URL = "/client/register"
FEATURES_URL = "/client/features"
METRICS_URL = "/client/metrics"

# Cache keys
FAILED_STRATEGIES = 'failed_strategies'
ETAG = 'etag'
