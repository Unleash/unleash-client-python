#!/bin/bash
set -ex

# Install package
python setup.py install
./get-spec.sh

# Install pre-config
# pip install pre-commit
# pre-commit install
# pre-commit

# Configure git
git config --global --add --bool push.autoSetupRemote true

# Woohoo!
echo "Hooray, it's done!"
