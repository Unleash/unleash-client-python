from UnleashClient.utils import LOGGER


class BackoffStrategy:
    def __init__(self):
        self.failures = 0
        self.skips = 0
        self.max_skips = 10
        self.normal_interval_seconds = 5
        self.longest_acceptable_interval_seconds = 60 * 60 * 24 * 7  # 1 week
        self.initialized = (
            False  # Consider not initialized until we have a successful call to the API
        )

    def handle_response(self, url: str, status_code: int):
        if self.initialized and status_code in [401, 403, 404]:
            self.skips = self.max_skips
            self.failures += 1
            LOGGER.error(
                f"Server said that the endpoint at {url} does not exist. Backing off to {self.skips} times our poll interval (of {self.normal_interval_seconds} seconds) to avoid overloading server"
                if status_code == 404
                else f"Client was not authorized to talk to the Unleash API at {url}. Backing off to {self.skips} times our poll interval (of {self.normal_interval_seconds} seconds) to avoid overloading server"
            )

        elif self.initialized and status_code == 429:
            self.failures += 1
            self.skips = min(self.max_skips, self.failures)
            LOGGER.info(
                f"RATE LIMITED for the {self.failures} time. Further backing off. Current backoff at {self.skips} times our interval (of {self.normal_interval_seconds} seconds)"
            )
        elif self.initialized and status_code > 500:
            self.failures += 1
            self.skips = min(self.max_skips, self.failures)
            LOGGER.info(
                f"Server failed with a {status_code} status code. Backing off. Current backoff at {self.skips} times our poll interval (of {self.normal_interval_seconds} seconds)"
            )

        else:
            # successful response
            self.initialized = True
            if self.failures > 0:
                self.failures -= 1
                self.skips = max(0, self.failures)

    def performAction(self):
        return self.skips <= 0

    def skipped(self):
        self.skips -= 1
