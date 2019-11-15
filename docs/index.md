# unleash-client-python

Welcome to the Unleash Python client documentation!  This folder contains documentation related to the project.

## Installation

Check out the package on [Pypi](https://pypi.org/project/UnleashClient/)!

```
pip install UnleashClient
```

## Initialization

```
from UnleashClient import UnleashClient
client = UnleashClient("https://unleash.herokuapp.com/api", "My Program")
client.initialize_client()
```

To clean up gracefully:
```
client.destroy()
```

## Checking if a feature is enabled

A check of a simple toggle:
```Python
client.is_enabled("My Toggle")
```

Specifying a default value:
```Python
client.is_enabled("My Toggle", default_value=True)
```

Supplying application context:
```Python
app_context = {"userId": "test@email.com"}
client.is_enabled("User ID Toggle", app_context)
```

Supplying a fallback function:
```Python
def custom_fallback(feature_name: str, context: dict) -> bool:
    return True

client.is_enabled("My Toggle", fallback_function=custom_fallback)
```

- Must accept the fature name and context as an argument.
- Client will evaluate the fallback function only if exception occurs when calling the `is_enabled()` method i.e. feature flag not found or other general exception. 
- If both a `default_value` and `fallback_function` are supplied, client will define the default value by `OR`ing the default value and the output of the fallback function.

## Getting a variant

Checking for a variant:
```python
context = {'userId': '2'}  # Context must have userId, sessionId, or remoteAddr.  If none are present, distribution will be random.

variant = client.get_variant("MyvariantToggle", context)

print(variant)
> {
>    "name": "variant1",
>    "payload": {
>        "type": "string",
>        "value": "val1"
>        },
>    "enabled": True
> }
```

`select_variant()` supports the same arguments (i.e. fallback functions) as the `is_enabled()` method.

For more information about variants, see the [Beta feature documentation](https://unleash.github.io/docs/beta_features).

## Logging

Unleash Client uses the built-in logging facility to show information about errors, background jobs (feature-flag updates and metrics), et cetera.

It's highly recommended that users implement

To see what's going on when PoCing code, you can use the following:
```python
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

``` 
