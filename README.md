# unleash-client-python

![](https://github.com/unleash/unleash-client-python/workflows/CI/badge.svg?branch=main) [![Coverage Status](https://coveralls.io/repos/github/Unleash/unleash-client-python/badge.svg?branch=main)](https://coveralls.io/github/Unleash/unleash-client-python?branch=main) [![PyPI version](https://badge.fury.io/py/UnleashClient.svg)](https://badge.fury.io/py/UnleashClient) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/UnleashClient.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is the Python client for [Unleash](https://github.com/unleash/unleash).  It implements [Client Specifications 1.0](https://docs.getunleash.io/client-specification) and checks compliance based on spec in [unleash/client-specifications](https://github.com/Unleash/client-specification)

What it supports:
* Default activation strategies using 32-bit [Murmurhash3](https://en.wikipedia.org/wiki/MurmurHash)
* Custom strategies
* Full client lifecycle:
    * Client registers with Unleash server
    * Client periodically fetches feature toggles and stores to on-disk cache
    * Client periodically sends metrics to Unleash Server
* Tested on Linux (Ubuntu), OSX, and Windows

Check out the [project documentation](https://unleash.github.io/unleash-client-python/) and the [changelog](https://docs.getunleash.io/unleash-client-python/changelog.html).

## Installation

Check out the package on [Pypi](https://pypi.org/project/UnleashClient/)!

```bash
pip install UnleashClient
```

## For Flask Users

If you're looking into running Unleash from Flask, you might want to take a look at [_Flask-Unleash_, the Unleash Flask extension](https://github.com/Unleash/Flask-Unleash). The extension builds upon this SDK to reduce the amount of boilerplate code you need to write to integrate with Flask. Of course, if you'd rather use this package directly, that will work too.

## Usage

### Initialization

```python
from UnleashClient import UnleashClient

client = UnleashClient(
    url="https://unleash.herokuapp.com",
    app_name="my-python-app",
    custom_headers={'Authorization': '<API token>'})

client.initialize_client()
```

For more information about configuring `UnleashClient`, check out the [project reference docs](https://docs.getunleash.io/unleash-client-python/unleashclient.html)!

### Checking if a feature is enabled

A check of a simple toggle:
```python
client.is_enabled("my_toggle")
```

To supply application context, use the second positional argument:

```python
app_context = {"userId": "test@email.com"}
client.is_enabled("user_id_toggle", app_context)
```

#### Fallback function and default values

You can specify a fallback function for cases where the client doesn't recognize the toggle by using the `fallback_function` keyword argument:

```python
def custom_fallback(feature_name: str, context: dict) -> bool:
    return True

client.is_enabled("my_toggle", fallback_function=custom_fallback)
```

You can also use the `fallback_function` argument to replace the obsolete `default_value` keyword argument by using a lambda that ignores its inputs. Whatever the lambda returns will be used as the default value.

```python
client.is_enabled("my_toggle", fallback_function=lambda feature_name, context: True)
```

The fallback function **must** accept the feature name and context as positional arguments in that order.

The client will evaluate the fallback function only if an exception occurs when calling the `is_enabled()` method. This happens when the client can't find the feature flag. The client _may_ also throw other, general exceptions.

For more information about usage, see the [Usage documentation](https://docs.getunleash.io/unleash-client-python/usage.html).

### Getting a variant

Checking for a variant:
```python
context = {'userId': '2'}  # Context must have userId, sessionId, or remoteAddr.  If none are present, distribution will be random.

variant = client.get_variant("variant_toggle", context)

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

For more information about variants, see the [Variant documentation](https://docs.getunleash.io/advanced/toggle_variants).
