# pylint: disable=invalid-name, too-few-public-methods
import copy
import random
from typing import Dict, Optional  # noqa: F401

from UnleashClient import utils
from UnleashClient.constants import DISABLED_VARIATION

VARIANT_HASH_SEED = 86028157


class Variants:
    def __init__(
        self, variants_list: list, group_id: str, is_feature_variants: bool = True
    ) -> None:
        """
        Represents an A/B test

        variants_list = From the strategy document.
        """
        self.variants = variants_list
        self.group_id = group_id
        self.is_feature_variants = is_feature_variants

    def _apply_overrides(self, context: dict) -> dict:
        """
        Figures out if an override should be applied based on a context.

        Notes:
            - This matches only the first variant found.
        """
        variants_with_overrides = [x for x in self.variants if "overrides" in x.keys()]
        override_variant = {}  # type: Dict

        for variant in variants_with_overrides:
            for override in variant["overrides"]:
                identifier = utils.get_identifier(override["contextName"], context)
                if identifier in override["values"]:
                    override_variant = variant

        return override_variant

    @staticmethod
    def _get_seed(context: dict, stickiness_selector: str = "default") -> str:
        """Grabs seed value from context."""
        seed = ""

        if stickiness_selector == "default":
            if "userId" in context:
                seed = context["userId"]
            elif "sessionId" in context:
                seed = context["sessionId"]
            elif "remoteAddress" in context:
                seed = context["remoteAddress"]
            else:
                seed = str(random.random() * 10000)
        elif stickiness_selector == "random":
            seed = str(random.random() * 10000)
        else:
            seed = (
                context.get(stickiness_selector)
                or context.get("properties")[stickiness_selector]
            )

        return seed

    @staticmethod
    def _format_variation(variation: dict, flag_status: Optional[bool] = None) -> dict:
        formatted_variation = copy.deepcopy(variation)
        del formatted_variation["weight"]
        if "overrides" in formatted_variation:
            del formatted_variation["overrides"]
        if "stickiness" in formatted_variation:
            del formatted_variation["stickiness"]
        if "enabled" not in formatted_variation and flag_status is not None:
            formatted_variation["enabled"] = flag_status
        return formatted_variation

    def get_variant(self, context: dict, flag_status: Optional[bool] = None) -> dict:
        """
        Determines what variation a user is in.

        :param context:
        :param flag_status:
        :return:
        """
        if self.variants:
            override_variant = self._apply_overrides(context)
            if override_variant:
                return self._format_variation(override_variant, flag_status)

            total_weight = sum(x["weight"] for x in self.variants)
            if total_weight <= 0:
                return DISABLED_VARIATION

            stickiness_selector = (
                self.variants[0]["stickiness"]
                if "stickiness" in self.variants[0].keys()
                else "default"
            )

            target = utils.normalized_hash(
                self._get_seed(context, stickiness_selector),
                self.group_id,
                total_weight,
                seed=VARIANT_HASH_SEED,
            )
            counter = 0
            for variation in self.variants:
                counter += variation["weight"]

                if counter >= target:
                    return self._format_variation(variation, flag_status)

        # Catch all return.
        return DISABLED_VARIATION
