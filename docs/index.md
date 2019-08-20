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
