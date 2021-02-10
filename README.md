# unleash-client-python

![](https://github.com/unleash/unleash-client-python/workflows/CI/badge.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/Unleash/unleash-client-python/badge.svg?branch=master)](https://coveralls.io/github/Unleash/unleash-client-python?branch=master) [![PyPI version](https://badge.fury.io/py/UnleashClient.svg)](https://badge.fury.io/py/UnleashClient) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/UnleashClient.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is the Python client for [Unleash](https://github.com/unleash/unleash).  It implements [Client Specifications 1.0](https://github.com/Unleash/unleash/blob/master/docs/client-specification.md) and checks compliance based on spec in [unleash/client-specifications](https://github.com/Unleash/client-specification)

What it supports:
* Default activation strategies using 32-bit [Murmerhash3](https://en.wikipedia.org/wiki/MurmurHash)
* Custom strategies
* Full client lifecycle:
    * Client registers with Unleash server
    * Client periodically fetches feature toggles and stores to on-disk cache
    * Client periodically sends metrics to Unleash Server
* Tested on Linux (Ubuntu), OSX, and Windows

Check out the [project documentation](https://unleash.github.io/unleash-client-python/) and the [changelog](https://unleash.github.io/unleash-client-python/changelog/).

## Installation

Check out the package on [Pypi](https://pypi.org/project/UnleashClient/)!

```
pip install UnleashClient
```

## Usage

### Initialization

```
from UnleashClient import UnleashClient
client = UnleashClient("https://unleash.herokuapp.com/api", "My Program")
client.initialize_client()
```

To clean up gracefully:
```
client.destroy()
```

#### Arguments
Argument | Description | Required? |  Type |  Default Value|
---------|-------------|-----------|-------|---------------|
url      | Unleash server URL | Y | String | N/A |
app_name | Name of your program | Y | String | N/A |
environment | Name of current environment | N | String | default |
instance_id | Unique ID for your program | N | String | unleash-client-python |
refresh_interval | How often the unleash client should check for configuration changes. | N | Integer |  15 |
metrics_interval | How often the unleash client should send metrics to server. | N | Integer | 60 |
disable_metrics | Disables sending metrics to Unleash server. | N | Boolean | F |
disable_registration | Disables registration with Unleash server. | N | Boolean | F |
custom_headers | Custom headers to send to Unleash. | N | Dictionary | {} |
custom_strategies | Custom strategies you'd like UnleashClient to support. | N | Dictionary | {} |

### Checking if a feature is enabled

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

### Getting a variant

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

For more information about variants, see the [Variant documentation](https://unleash.github.io/docs/toggle_variants).
