import logging
import mmh3  # pylint: disable=import-error

LOGGER = logging.getLogger(__name__)


def normalized_hash(identifier: str,
                    activation_group: str) -> int:
    return mmh3.hash("{}:{}".format(identifier, activation_group)) % 100 + 1
