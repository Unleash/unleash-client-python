## UnleashClient

### `__init__()`
A client for the Unleash feature toggle system.

`
UnleashClient.__init__(url, app_name, instance_id, refresh_interval, metrics_interval, disable_metrics, disable_registration, custom_headers)
`

**Arguments**

Argument | Description | Required? |  Type |  Default Value|
---------|-------------|-----------|-------|---------------|
url      | Unleash server URL | Y | String | N/A |
app_name | Name of your program | Y | String | N/A |
instance_id | Unique ID for your program | N | String | unleash-client-python | 
refresh_interval | How often the unleash client should check for configuration changes. | N | Integer |  15 |
metrics_interval | How often the unleash client should send metrics to server. | N | Integer | 60 |
disable_metrics | Disables sending metrics to Unleash server. | N | Boolean | F |
disable_registration | Disables registration with Unleash server. | N | Boolean | F |
custom_headers | Custom headers to send to Unleash. | N | Dictionary | {}
custom_options | Custom arguments for requests package. | N | Dictionary | {}
custom_strategies | Custom strategies you'd like UnleashClient to support. | N | Dictionary | {} |
cache_directory | Location of the cache directory. When unset, FCache will determine the location | N | Str | Unset | 

### `initialize_client()`
Initializes client and starts communication with central unleash server(s).

This kicks off:
* Client registration
* Provisioning poll
* Stats poll

### `destroy()`
Gracefully shuts down the Unleash client by stopping jobs, stopping the scheduler, and deleting the cache.

You shouldn't need this too much!

### `is_enabled()`

Checks if a feature toggle is enabled.

Notes:
* If client hasn't been initialized yet or an error occurs, flat will default to false.

`
UnleashClient.is_enabled(feature_name, context, default_value)
`

**Arguments**

Argument | Description | Required? |  Type |  Default Value|
---------|-------------|-----------|-------|---------------|
feature_name | Name of feature | Y | String | N/A |
context | Custom information for strategies | N | Dictionary | {} |
default_value | Deprecated, use Fallback Function. | N | Boolean | F |
fallback_function | A function that takes two arguments (feature name, context) and returns a boolean.  Used if exception occurs when checking a feature flag. | N | Callable | None |

### Notes

**Using `unleash-client-python` with Gitlab** 

[Gitlab's feature flags](https://docs.gitlab.com/ee/user/project/operations/feature_flags.html) only supports the features URL.  (API calls to the registration URL and metrics URL will fail with HTTP Error code 401.)

If using `unleash-client-python` with Gitlab's feature flages, we recommend initializing the client with `disable_metrics` = True and `disable_registration` = True.

``` python
my_client = UnleashClient(
    url="https://gitlab.com/api/v4/feature_flags/someproject/someid",
    app_name="myClient1",
    instance_id="myinstanceid",
    disable_metrics=True,
    disable_registration=True
)
```

**Overriding SSL certificate verification**

(Do this at your own risk!)

If using an on-prem SSL certificate with a self-signed cert, you can pass custom arguments through to the **request** package using the *custom_options* argument.

```python
my_client = UnleashClient(
    url="https://myunleash.hamster.com",
    app_name="myClient1",
    instance_id="myinstanceid",
    custom_options={"verify": False}
)
```
