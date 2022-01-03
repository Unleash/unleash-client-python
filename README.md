# unleash-client-python

![](https://github.com/unleash/unleash-client-python/workflows/CI/badge.svg?branch=main) [![Coverage Status](https://coveralls.io/repos/github/Unleash/unleash-client-python/badge.svg?branch=main)](https://coveralls.io/github/Unleash/unleash-client-python?branch=main) [![PyPI version](https://badge.fury.io/py/UnleashClient.svg)](https://badge.fury.io/py/UnleashClient) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/UnleashClient.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is the Python client for [Unleash](https://github.com/unleash/unleash).  It implements [Client Specifications 1.0](https://github.com/Unleash/unleash/blob/main/docs/client-specification.md) and checks compliance based on spec in [unleash/client-specifications](https://github.com/Unleash/client-specification)

What it supports:
* Default activation strategies using 32-bit [Murmurhash3](https://en.wikipedia.org/wiki/MurmurHash)
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

## For Flask Users

If you're looking into running Unleash from Flask, you might want to take a look at [_Flask-Unleash_, the Unleash Flask extension](https://github.com/Unleash/Flask-Unleash). The extension builds upon this SDK to reduce the amount of boilerplate code you need to write to integrate with Flask. Of course, if you'd rather use this package directly, that will work too.

## Usage

### Initialization

```Python
from UnleashClient import UnleashClient

client = UnleashClient(
    url="https://unleash.herokuapp.com",
    app_name="my-python-app",
    custom_headers={'Authorization': '<API token>'})

client.initialize_client()
```

If you're running Unleash in a Docker container or self hosting, your URL should look like `http://localhost:4242/api` (with the `/api` suffix).

To clean up gracefully:
```Python
client.destroy()
```

If the client is already initialized, calling `initialize_client()` again will raise a warning.  This is not recommended client usage as it results in unneccessary calls to the Unleash server.

#### Arguments
Argument | Description | Required? |  Type |  Default Value|
---------|-------------|-----------|-------|---------------|
url      | Unleash server URL | Y | String | N/A |
app_name | Name of your program | Y | String | N/A |
environment | Name of current environment | N | String | default |
instance_id | Unique ID for your program | N | String | unleash-client-python |
refresh_interval | How often the unleash client should check for configuration changes. | N | Integer |  15 |
refresh_jitter | Maximum delay added to refresh interval value. | N | Integer |  None |
metrics_interval | How often the unleash client should send metrics to server. | N | Integer | 60 |
metrics_jitter | Maximum delay added to sending metrics to server interval. | N | Integer | None |
disable_metrics | Disables sending metrics to Unleash server. | N | Boolean | F |
disable_registration | Disables registration with Unleash server. | N | Boolean | F |
custom_headers | Custom headers to send to Unleash. | N | Dictionary | {} |
custom_strategies | Custom strategies you'd like UnleashClient to support. | N | Dictionary | {} |
cache_directory | Location of the cache directory. When unset, FCache will determine the location | N | Str | Unset |
project_name | Unleash project Id to load feature flags from | N | Str | "" |
verbose_log_level | Numerical log level (https://docs.python.org/3/library/logging.html#logging-levels) for cases where checking a feature flag fails. | N | Integer | 30 (Warning) |

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

For more information about variants, see the [Variant documentation](https://docs.getunleash.io/advanced/toggle_variants).


### Running in a WSGI Context


WSGI is a fairly common way of running webserver applications for both Flask and Django, if you're running in WSGI there are a few caveats that you should be aware of:

* By default WSGI removes the GIL and disables threading, this SDK requires threads to work for the background updates of feature toggles, without it, your application will run but will not reflect updates to state of feature toggles when changed. To get around this, you'll need to enable threading, you can do this by setting enable-threads in your WSGI configuration

* If you need to scale out your application with multiple processes by setting the processes flag in your WSGI configuration, note that this can cause issues with updates as well, in order to resolve these, you'll also need to enable the lazy-apps flag in WSGI, this will cause each process to trigger a clean reload of your application. More information on the rammifcations of this change can be found [here](https://uwsgi-docs.readthedocs.io/en/latest/articles/TheArtOfGracefulReloading.html#preforking-vs-lazy-apps-vs-lazy)
