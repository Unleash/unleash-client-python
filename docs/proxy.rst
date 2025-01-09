Proxy Configuration
====================

To connect to a proxy, you need to run the proxy container with the additional parameter ``EXP_SERVER_SIDE_SDK_CONFIG_TOKENS``. **Note:** This is an experimental feature. For more details, refer to the `Unleash Proxy Documentation <https://docs.getunleash.io/reference/unleash-proxy#experimental-configuration-options>`_.

Step 1: Running the Proxy Container
------------------------------------

Execute the following Docker command to run the proxy container with the necessary environment variables:

.. code-block:: bash

    docker run \
        -e UNLEASH_PROXY_CLIENT_KEYS=<proxy-client-key> \
        -e UNLEASH_URL='<unleash-api-url>' \
        -e UNLEASH_API_TOKEN=<client-api-token> \
        -e EXP_SERVER_SIDE_SDK_CONFIG_TOKENS=<server-sdk-token> \
        -p 3000:3000 \
        unleashorg/unleash-proxy

Replace the following placeholders:

- ``<proxy-client-key>``: Your proxy client key.  
- ``<unleash-api-url>``: The URL of your Unleash API.   
- ``<client-api-token>``: Your Unleash API token.   
- ``<server-sdk-token>``: The server SDK token (used for the experimental configuration).  

Step 2: Connecting to the Proxy
--------------------------------

Once the proxy is running, you can connect to it by passing the server SDK token in the request header. Here's an example of how to set up the Unleash client:

.. code-block:: python

    client = UnleashClient(
        url='<unleash-proxy-url>',
        app_name='<app-name>',
        custom_headers={'Authorization': '<server-sdk-token>'},
    )

Replace the following placeholders:

- ``<unleash-proxy-url>``: The URL of your Unleash proxy, for example, ``http://localhost:3000/proxy``.
- ``<app-name>``: The name of your application.
- ``<server-sdk-token>``: The server SDK token used to authenticate the request.
