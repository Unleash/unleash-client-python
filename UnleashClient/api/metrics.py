import json
import requests
from UnleashClient.constants import REQUEST_TIMEOUT, APPLICATION_HEADERS, METRICS_URL
from UnleashClient.utils import LOGGER


# pylint: disable=broad-except
def send_metrics(url: str,
                 request_body: dict,
                 custom_headers: dict) -> bool:
    """
    Attempts to send metrics to Unleash server

    Notes:
    * If unsuccessful (i.e. not HTTP status code 200), message will be logged

    :param url:
    :param app_name:
    :param instance_id:
    :param metrics_interval:
    :param custom_headers:
    :return: true if registration successful, false if registration unsuccessful or exception.
    """
    try:
        LOGGER.info("Sending messages to with unleash @ %s", url)
        LOGGER.info("unleash metrics information: %s", request_body)

        resp = requests.post(url + METRICS_URL,
                             data=json.dumps(request_body),
                             headers={**custom_headers, **APPLICATION_HEADERS},
                             timeout=REQUEST_TIMEOUT)

        if resp.status_code != 202:
            LOGGER.warning("unleash metrics submission failed.")
            return False

        LOGGER.info("unleash metrics successfully sent!")

        return True
    except Exception:
        LOGGER.exception("unleash metrics failed to send.")

    return False
