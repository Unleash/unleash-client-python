#!/bin/bash
specversion=$(python -c "from UnleashClient.constants import CLIENT_SPEC_VERSION; print(CLIENT_SPEC_VERSION)")

rm -rf tests/specification_tests/client-specification
echo "Downloading client spec ${specversion}"
git clone --depth 5 --branch v"${specversion}" https://github.com/Unleash/client-specification.git tests/specification_tests/client-specification
