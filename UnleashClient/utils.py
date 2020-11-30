import logging
import mmh3  # pylint: disable=import-error
from requests import Response

LOGGER = logging.getLogger(__name__)


def normalized_hash(identifier: str,
                    activation_group: str,
                    normalizer: int = 100) -> int:
    return mmh3.hash("{}:{}".format(activation_group, identifier), signed=False) % normalizer + 1


def get_identifier(context_key_name: str, context: dict) -> str:
    if context_key_name in context.keys():
        value = context[context_key_name]
    elif 'properties' in context.keys() and context_key_name in context['properties'].keys():
        value = context['properties'][context_key_name]
    else:
        value = None

    return value


def log_resp_info(resp: Response) -> None:
    LOGGER.debug("HTTP status code: %s", resp.status_code)
    LOGGER.debug("HTTP headers: %s", resp.headers)
    LOGGER.debug("HTTP content: %s", resp.text)
