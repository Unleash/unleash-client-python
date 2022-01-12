****************************************
Running with WSGI
****************************************

WSGI is a fairly common way of running webserver applications for both Flask and Django, if you're running in WSGI there are a few caveats that you should be aware of:

- By default WSGI removes the GIL and disables threading, this SDK requires threads to work for the background updates of feature toggles, without it, your application will run but will not reflect updates to state of feature toggles when changed. To get around this, you'll need to enable threading, you can do this by setting enable-threads in your WSGI configuration
- If you need to scale out your application with multiple processes by setting the processes flag in your WSGI configuration, note that this can cause issues with updates as well, in order to resolve these, you'll also need to enable the lazy-apps flag in WSGI, this will cause each process to trigger a clean reload of your application. More information on the rammifcations of this change can be found `here <https://uwsgi-docs.readthedocs.io/en/latest/articles/TheArtOfGracefulReloading.html#preforking-vs-lazy-apps-vs-lazy>`_.
