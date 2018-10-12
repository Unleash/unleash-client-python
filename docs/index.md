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
client = UnleashClient("https://unleash.herokuapp.com", "My Program")
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
