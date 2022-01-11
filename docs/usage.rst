****************************************
Usage
****************************************

Initialization
#######################################

.. code-block:: python

    from UnleashClient import UnleashClient
    client = UnleashClient("https://unleash.herokuapp.com/api", "My Program")
    client.initialize_client()

To clean up gracefully:

.. code-block:: python

    client.destroy()

If the client is already initialized, calling ``initialize_client()`` again will raise a warning.  This is not recommended client usage as it results in unneccessary calls to the Unleash server.

Checking if a feature is enabled
#######################################

A check of a simple toggle:

.. code-block:: python

    client.is_enabled("My Toggle")


Specifying a default value:

.. code-block:: python

    client.is_enabled("My Toggle", default_value=True)


Supplying application context:

.. code-block:: python

    app_context = {"userId": "test@email.com"}
    client.is_enabled("User ID Toggle", app_context)

Supplying a fallback function:

.. code-block:: python

    def custom_fallback(feature_name: str, context: dict) -> bool:
    return True

    client.is_enabled("My Toggle", fallback_function=custom_fallback)

Notes:

- Must accept the fature name and context as an argument.
- Client will evaluate the fallback function only if exception occurs when calling the ``is_enabled()`` method i.e. feature flag not found or other general exception.
- If both a ``default_value`` and ``fallback_function`` are supplied, client will define the default value by ``OR`` ing the default value and the output of the fallback function.


Getting a variant
#######################################

Checking for a variant:

.. code-block:: python

    context = {'userId': '2'}  # Context must have userId, sessionId, or remoteAddr.  If none are present, distribution will be random.

    variant = client.get_variant("MyvariantToggle", context)

    print(variant)

Returns:

.. code-block::

    {
       "name": "variant1",
       "payload": {
           "type": "string",
           "value": "val1"
           },
       "enabled": True
    }


``select_variant()`` supports the same arguments (i.e. fallback functions) as the ``is_enabled()`` method.

For more information about variants, see the `Variable documentation <https://docs.getunleash.io/advanced/toggle_variants>`_.

Logging
#######################################

Unleash Client uses the built-in logging facility to show information about errors, background jobs (feature-flag updates and metrics), et cetera.

It's highly recommended that users implement

To see what's going on when PoCing code, you can use the following:

.. code-block:: python

    import logging
    import sys

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)
