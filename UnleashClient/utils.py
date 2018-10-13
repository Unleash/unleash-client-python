import logging
import mmh3  # pylint: disable=import-error

LOGGER = logging.getLogger(__name__)


def normalized_hash(identifier: str,
                    activation_group: str) -> int:
    return mmh3.hash("{}:{}".format(activation_group, identifier), signed=False) % 100 + 1
