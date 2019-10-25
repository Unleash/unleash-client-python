from UnleashClient import utils


class Variants():
    def __init__(self, variants_list: list) -> None:
        """
        Represents an A/B test

        variants_list = From the strategy document.
        """
        self.variants = variants_list

    def _apply_overrides(self, context: dict) -> dict:
        """
        Figures out if an override should be applied based on a context.

        Notes:
            - This matches only the first varient found.
        """
        variants_with_overrides = [x for x in self.variants if 'overrides' in x.keys()]
        override_variant: dict = {}

        for variant in variants_with_overrides:
            for override in variant['overrides']:
                identifier = utils.get_identifier(override['contextName'], context)
                if identifier in override["values"]:
                    override_variant = variant

        return override_variant

    def select_variant(self, context: dict) -> dict:
        """
        Determines what variation a user is in.

        :param context:
        :return:
        """
