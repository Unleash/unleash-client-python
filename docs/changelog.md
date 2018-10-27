## v1.0.2

General
* unleash-client-python has moved under the general Unleash project!

## v1.0.0
**General**
* Implemented custom strategies. 

## v0.3.0

**General**
* Implemented [client specification](https://github.com/Unleash/client-specification) tests.
* Cache changed to use Instance ID as key.

**Bugfixes**
* (Major) Fixed interposed arguments in normalized_hash() (aka MurmerHash3 wrapper).  Python client will now do the same thing as the other clients!
* (Major) Fixed issues with logic in random strategies.

## v0.2.0

**General**
* Changed cache implementation.  Instead of caching {feature toggle name: provisioning} we'll now cache the entire API response (and use it if the fetch fails in any way).

## v0.1.1

**General**
* Fixed Github link on pypi.
* Removed unused sphinx documentation.
* Added documentation using mkdocs

## v0.1.0

**General**
* First implementation of the Unleash Python client!  Woo!
