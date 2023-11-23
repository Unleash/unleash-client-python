import json
from datetime import datetime, timezone

import requests
from requests.exceptions import InvalidHeader, InvalidSchema, InvalidURL, MissingSchema

from UnleashClient.constants import (
    APPLICATION_HEADERS,
    REGISTER_URL,
    REQUEST_TIMEOUT,
    SDK_NAME,
    SDK_VERSION,
)
from UnleashClient.utils import LOGGER, log_resp_info


# pylint: disable=broad-except
def register_client(
    url: str,
    app_name: str,
    instance_id: str,
    metrics_interval: int,
    custom_headers: dict,
    custom_options: dict,
    supported_strategies: dict,
    request_timeout=REQUEST_TIMEOUT,
) -> bool:
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
    :param custom_options:
    :param supported_strategies:
    :return: true if registration successful, false if registration unsuccessful or exception.
    """
    registation_request = {
        "appName": app_name,
        "instanceId": instance_id,
        "sdkVersion": f"{SDK_NAME}:{SDK_VERSION}",
        "strategies": [*supported_strategies],
        "started": datetime.now(timezone.utc).isoformat(),
        "interval": metrics_interval,
    }

    try:
        LOGGER.info("Registering unleash client with unleash @ %s", url)
        LOGGER.info("Registration request information: %s", registation_request)

        resp = requests.post(
            url + REGISTER_URL,
            data=json.dumps(registation_request),
            headers={**custom_headers, **APPLICATION_HEADERS},
            timeout=request_timeout,
            **custom_options,
        )

        if resp.status_code != 202:
            log_resp_info(resp)
            LOGGER.warning(
                "Unleash Client registration failed due to unexpected HTTP status code."
            )
            return False

        LOGGER.info("Unleash Client successfully registered!")

        return True
    except (MissingSchema, InvalidSchema, InvalidHeader, InvalidURL) as exc:
        LOGGER.exception(
            "Unleash Client registration failed fatally due to exception: %s", exc
        )
        raise exc
    except requests.RequestException as exc:
        LOGGER.exception("Unleash Client registration failed due to exception: %s", exc)

    return False
