****************************************
Running with Celery
****************************************

To use this client with Celery, call the `initialize_client` method in the `worker_process_init` event. If you don't initialize the client inside the `worker_process_init` event, the client will not poll for updates. As such, the client will not update its feature toggles, even when changes are made server side.

.. code-block:: python

    from UnleashClient import UnleashClient
    from celery.signals import worker_process_init

    client = UnleashClient(
        url="http://localhost:4242/api/",
        app_name="test-dev",
        custom_headers={'Authorization': '*:development.bb09e81624d5ad67b2ac29bd0b0fdc35ccbac884e63cfd20c6fefc49'})

    @worker_process_init.connect
    def configure_workers(sender=None, conf=None, **kwargs):
        client.initialize_client()
