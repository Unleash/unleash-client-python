# Migrating to Unleash-Client-Python 6.0.0

This guide highlights the key changes you should be aware of when upgrading to v6.0.0 of the Unleash client.

## Removed direct access to feature flags

Direct access to the feature flag objects through `UnleashClient.features` has been removed. All classes related to the internal representation of feature flags are no longer publicly accessible in the SDK.

The SDK now provides an `UnleashClient.feature_definitions()` method, which returns a list of feature flag names, their type, and the project they're bound to.

## Changes to custom strategies

Custom strategies have undergone some changes that require updates to their implementations. This is a strict requirement: any strategy that does not implement the correct interface will throw an exception at startup.

The interface changes are as follows:

- Strategies no longer inherit from a base class.
- The apply method now accepts a second parameter, `parameters`. In legacy versions, this functionality was managed by the `load_provisioning()` method.

Here is an example of a legacy strategy:

``` python
class CatStrategy(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["sound"].split(",")]

    def apply(self, context: dict = None) -> bool:
        default_value = False

        if "sound" in context.keys():
            default_value = context["sound"] in self.parsed_provisioning

        return default_value
```

This is now written as:

``` python
class CatStrategy:
    def apply(self, parameters: dict, context: dict = None) -> bool:
        default_value = False

        parsed_parameters = [x.strip() for x in parameters["sound"].split(",")]

        if "sound" in context.keys():
            default_value = context["sound"] in parsed_parameters

        return default_value

```

Strategies are now mounted as an instance rather than a class object when configuring the SDK:

``` python

custom_strategies_dict = {"amIACat": CatStrategy()}

unleash_client = UnleashClient(
    "some_unleash_url", "some_app_name", custom_strategies=custom_strategies_dict
)

```
