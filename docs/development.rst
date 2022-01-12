****************************************
Development
****************************************

Contributions welcome!  

Here are some notes about common tools and tasks you'll run into when working on `unleash-client-python`.

Tooling
#######################################

- `Pyenv <https://github.com/pyenv/pyenv>`_ for managing Python versions.

Testing
#######################################

1. Activate your virtualenv solution (e.g. `source activate YOUR_VIRTUALENV`).
2. Run linting & tests: ``make test``

Release
#######################################

1. Land all your PRs on `main`!
2. If new configuration is added, update `Flask-Unleash <https://github.com/Unleash/Flask-Unleash>`_ config.
3. Update changelog.md and other documentation.
4. Create tag on `main` branch.
5. Create new Release in Github and paste in changelog.
6. Github Actions workflow will automagically publish to Pypi and build documentation.
7. Publish new Flask-Unleash package (if necessary).

Snippets
#######################################

Serving docs from WSL!

.. code-block:: shell

    docker run -d --name unleash-docs --rm -v `pwd`/_build/html:/web -p 8080:8080 halverneus/static-file-server:latest
