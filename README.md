# unleash-client-python

[![CircleCI](https://circleci.com/gh/ivanklee86/unleash-client-python.svg?style=svg)](https://circleci.com/gh/ivanklee86/unleash-client-python) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Coverage Status](https://coveralls.io/repos/github/ivanklee86/unleash-client-python/badge.svg?branch=il%2FI-8_releaseprep)](https://coveralls.io/github/ivanklee86/unleash-client-python?branch=il%2FI-8_releaseprep)


This is a Python client for Unleash.  It strives to [Client Specifications 1.0](https://github.com/Unleash/unleash/blob/master/docs/client-specification.md) (though as this project is still very much a work in progress!).

What it supports:
* Default activation strategies using 32-bit [Murmerhash3](https://en.wikipedia.org/wiki/MurmurHash)
* Client registration
* Periodically fetching feature flags
* Caching of feature-flag provisioning
* Periodically sending metrics

What it doesn't:
* Custom strategies

Read more about the Unleash project [here](https://github.com/unleash/unleash).

## Installation
TODO: Put on Pypi. :)

```
pip install UnleashClient
```

## Usage

### Initialization

```
from UnleashClient import UnleashClient
client = UnleashClient("https://unleash.herokuapp.com", "My Program")
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
instance_id | Unique ID for your program | N | String | unleash-client-python | 
refresh_interval | How often the unleash client should check for configuration changes. | N | Integer |  15 |
metrics_interval | How often the unleash client should send metrics to server. | N | Integer | 60 |
disable_metrics | Disables sending metrics to Unleash server. | N | Boolean | F |
custom_headers | Custom headers to send to Unleash. | N | Dictionary | {}

### Checking if a feature is enabled

A check of a simple toggle:
```
client.is_enabled("My Toggle")
```

Specifying a default value:
```
client.is_enabled("My Toggle", default_value=True)
```

Supplying application context:
```
app_context = {"userId": "test@email.com"}
client.is_enabled("User ID Toggle", app_context)
```
