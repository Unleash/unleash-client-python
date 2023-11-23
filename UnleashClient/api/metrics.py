import json

import requests

from UnleashClient.constants import APPLICATION_HEADERS, METRICS_URL, REQUEST_TIMEOUT
from UnleashClient.utils import LOGGER, log_resp_info


# pylint: disable=broad-except
def send_metrics(
    url: str,
    request_body: dict,
    custom_headers: dict,
    custom_options: dict,
    request_timeout: int = REQUEST_TIMEOUT,
) -> bool:
    """
    Attempts to send metrics to Unleash server

    Notes:
    * If unsuccessful (i.e. not HTTP status code 200), message will be logged

    :param url:
    :param request_body:
    :param custom_headers:
    :param custom_options:
    :return: true if registration successful, false if registration unsuccessful or exception.
    """
    try:
        LOGGER.info("Sending messages to with unleash @ %s", url)
        LOGGER.info("unleash metrics information: %s", request_body)

        resp = requests.post(
            url + METRICS_URL,
            data=json.dumps(request_body),
            headers={**custom_headers, **APPLICATION_HEADERS},
            timeout=request_timeout,
            **custom_options,
        )

        if resp.status_code != 202:
            log_resp_info(resp)
            LOGGER.warning("Unleash CLient metrics submission failed.")
            return False

        LOGGER.info("Unleash Client metrics successfully sent!")

        return True
    except requests.RequestException as exc:
        LOGGER.warning(
            "Unleash Client metrics submission failed due to exception: %s", exc
        )

    return False
