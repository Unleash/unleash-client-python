import requests
from UnleashClient.constants import REQUEST_TIMEOUT, FEATURES_URL
from UnleashClient.utils import LOGGER, log_resp_info


# pylint: disable=broad-except
def get_feature_toggles(url: str,
                        app_name: str,
                        instance_id: str,
                        custom_headers: dict,
                        custom_options: dict,
                        project: str = None) -> dict:
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
    :return: Feature flags if successful, empty dict if not.
    """
    try:
        LOGGER.info("Getting feature flag.")

        headers = {
            "UNLEASH-APPNAME": app_name,
            "UNLEASH-INSTANCEID": instance_id
        }

        base_url = f"{url}{FEATURES_URL}"
        base_params = {}

        if project:
            base_params = {'project': project}

        resp = requests.get(base_url,
                            headers={**custom_headers, **headers},
                            params=base_params,
                            timeout=REQUEST_TIMEOUT, **custom_options)

        if resp.status_code != 200:
            log_resp_info(resp)
            LOGGER.warning("Unleash Client feature fetch failed due to unexpected HTTP status code.")
            raise Exception("Unleash Client feature fetch failed!")

        return resp.json()
    except Exception as exc:
        LOGGER.exception("Unleash Client feature fetch failed due to exception: %s", exc)

    return {}
