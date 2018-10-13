import json
import datetime
import requests
from UnleashClient.constants import SDK_NAME, SDK_VERSION, REQUEST_TIMEOUT, APPLICATION_HEADERS, REGISTER_URL
from UnleashClient.utils import LOGGER


# pylint: disable=broad-except
def register_client(url: str,
                    app_name: str,
                    instance_id: str,
                    metrics_interval: int,
                    custom_headers: dict,
                    supported_strategies: dict) -> bool:
    """
    Attempts to register client with unleash server.

    Notes:
    * If unsuccessful (i.e. not HTTP status code 202), exception will be caught and logged.
      This is to allow "safe" error handling if unleash server goes down.

    :param url:
    :param app_name:
    :param instance_id:
    :param metrics_interval:
    :param custom_headers:
    :param supported_strategies:
    :return: true if registration successful, false if registration unsuccessful or exception.
    """
    registation_request = {
        "appName": app_name,
        "instanceId": instance_id,
        "sdkVersion": "{}:{}".format(SDK_NAME, SDK_VERSION),
        "strategies": [*supported_strategies],
        "started": datetime.datetime.now().isoformat(),
        "interval": metrics_interval
    }

    try:
        LOGGER.info("Registering unleash client with unleash @ %s", url)
        LOGGER.info("Registration request information: %s", registation_request)

        resp = requests.post(url + REGISTER_URL,
                             data=json.dumps(registation_request),
                             headers={**custom_headers, **APPLICATION_HEADERS},
                             timeout=REQUEST_TIMEOUT)

        if resp.status_code != 202:
            LOGGER.warning("unleash client registration failed.")
            return False

        LOGGER.info("unleash client successfully registered!")

        return True
    except Exception:
        LOGGER.exception("unleash client registration failed.")

    return False
