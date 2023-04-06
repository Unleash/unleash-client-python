#!/bin/bash
set -ex

# Install package
sudo su - vscode bash -c "cd /workspaces/unleash-client-python; python -m venv .venv; source .venv/bin/activate; pip install -U -r requirements.txt; python setup.py install; ./get-spec.sh;"

# Install pre-config
# pip install pre-commit
# pre-commit install
# pre-commit

# Configure git
git config --global --add --bool push.autoSetupRemote true

# Woohoo!
echo "Hooray, it's done!"
