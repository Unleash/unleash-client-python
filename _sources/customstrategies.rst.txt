****************************************
Custom Strategies
****************************************

Implementing a custom strategy
#######################################

- Set up a custom strategy in Unleash.  Note down the name - you'll need this exact value to ensure we're loading the custom strategy correctly.
- Create a custom strategy object by sub-classing the Strategy object.

.. code-block:: python

    from UnleashClient.strategies.Strategies import Strategy

    class CatTest(Strategy):
        def load_provisioning(self) -> list:
            return [x.strip() for x in self.parameters["sound"].split(',')]

        def apply(self, context: dict = None) -> bool:
            """
            Turn on if I'm a cat.

            :return:
            """
            default_value = False

            if "sound" in context.keys():
                default_value = context["sound"] in self.parsed_provisioning

            return default_value


- Create a dictionary where the key is the name of the custom strategy.  Note: The key must match the name of the custom strategy created on the Unleash server exactly (including capitalization!).

.. code-block:: python

    my_custom_strategies = {"amIACat": CatTest}

- When initializing UnleashClient, provide the custom strategy dictionary.

.. code-block:: python

    unleash_client = UnleashClient(URL, APP_NAME, custom_strategies=my_custom_strategies)

- Fire up Unleash! You can now use the "amIACat" strategy in a feature toggle.

Migrating your custom strategies from Strategy from v2.x.x to v3.x.x (for fun and profit)
#########################################################################################
To get support for for constraints in your custom strategy, take the following steps:

- Instead of overriding the `__call__()` method, override the `apply()` method.  (In practice, you can just rename the method!)
- ???
- Profit!
