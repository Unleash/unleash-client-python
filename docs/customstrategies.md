## Implementing a custom strategy

* Set up a custom strategy in Unleash.  Note down the name - you'll need this exact value to ensure we're loading the custom strategy correctly.
* Create a custom strategy object by sub-classing the Strategy object. 

```
from UnleashClient.strategies import Strategy

class CatTest(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(',')]

    def __call__(self, context: dict = None) -> bool:
        """
        Turn on if I'm a cat.

        :return:
        """
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value
```

* Create a dictionary where the key is the name of the custom strategy.

```
my_custom_strategies = {"amIACat": CatTest}
```

* When initializing UnleashClient, provide the custom strategy dictionary.

```
unleash_client = UnleashClient(URL, APP_NAME, custom_strategies=my_custom_strategies)
```

* Fire up Unleash! You can now use the "amIACat" strategy in a feature toggle.
