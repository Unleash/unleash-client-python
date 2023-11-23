from typing import Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from UnleashClient.constants import FEATURES_URL, REQUEST_RETRIES, REQUEST_TIMEOUT
from UnleashClient.utils import LOGGER, log_resp_info


# pylint: disable=broad-except
def get_feature_toggles(
    url: str,
    app_name: str,
    instance_id: str,
    custom_headers: dict,
    custom_options: dict,
    project: Optional[str] = None,
    cached_etag: str = "",
    request_timeout: int = REQUEST_TIMEOUT,
    request_retries: int = REQUEST_RETRIES,
) -> Tuple[dict, str]:
    """
    Retrieves feature flags from unleash central server.

    Notes:
    * If unsuccessful (i.e. not HTTP status code 200), exception will be caught and logged.
      This is to allow "safe" error handling if unleash server goes down.

    :param url:
    :param app_name:
    :param instance_id:
    :param custom_headers:
    :param custom_options:
    :param project:
    :param cached_etag:
    :return: (Feature flags, etag) if successful, ({},'') if not
    """
    try:
        LOGGER.info("Getting feature flag.")

        headers = {"UNLEASH-APPNAME": app_name, "UNLEASH-INSTANCEID": instance_id}

        if cached_etag:
            headers["If-None-Match"] = cached_etag

        base_url = f"{url}{FEATURES_URL}"
        base_params = {}

        if project:
            base_params = {"project": project}

        adapter = HTTPAdapter(
            max_retries=Retry(total=request_retries, status_forcelist=[500, 502, 504])
        )
        with requests.Session() as session:
            session.mount("https://", adapter)
            session.mount("http://", adapter)
            resp = session.get(
                base_url,
                headers={**custom_headers, **headers},
                params=base_params,
                timeout=request_timeout,
                **custom_options,
            )

        if resp.status_code not in [200, 304]:
            log_resp_info(resp)
            LOGGER.warning(
                "Unleash Client feature fetch failed due to unexpected HTTP status code."
            )
            raise Exception(
                "Unleash Client feature fetch failed!"
            )  # pylint: disable=broad-exception-raised

        etag = ""
        if "etag" in resp.headers.keys():
            etag = resp.headers["etag"]

        if resp.status_code == 304:
            return None, etag

        return resp.json(), etag
    except Exception as exc:
        LOGGER.exception(
            "Unleash Client feature fetch failed due to exception: %s", exc
        )

    return {}, ""
