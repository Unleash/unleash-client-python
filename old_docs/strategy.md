## Strategy

### `__init__(params)`

A generic strategy objects.

**Arguments**

Argument | Description | Required? |  Type |  Default Value|
---------|-------------|-----------|-------|---------------|
params   | 'parameters' key from strategy section (...from feature section) of /api/clients/features response | N, but you probably should have one. :) | Dictionary | {} |

### `load_provisioning()`

Method to load data on object initialization, if desired.  This should parse the raw values in _self.parameters_ into format Python can comprehend.

The value returned by `load_provisioning()` will be stored in the _self.parsed_provisioning_ class variable when object is created.  The superclass returns an empty list since most of Unleash's default strategies are list-based (in one way or another).

## `apply(context)`
Strategy implementation goes here.

**Arguments**

Argument | Description | Required? |  Type |  Default Value|
---------|-------------|-----------|-------|---------------|
context   | Application Context | N | Dictionary | {} |