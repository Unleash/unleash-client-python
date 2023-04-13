SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = UnleashClient

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------
test: lint pytest specification-test

precommit: clean generate-requirements

build: clean build-package upload

build-local: clean build-package

#-----------------------------------------------------------------------
# Install
#-----------------------------------------------------------------------

install:
	pip install -U -r requirements.txt && \
	python setup.py install && \
	./get-spec.sh

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------
fix:
	black . && \
	ruff UnleashClient tests --fix

lint:
	black . --check && \
	ruff UnleashClient tests && \
	mypy ${PROJECT_NAME} --install-types --non-interactive;

pytest:
	export PYTHONPATH="${ROOT_DIR}:$$PYTHONPATH" && \
	py.test tests/unit_tests

specification-test:
	export PYTHONPATH="${ROOT_DIR}:$$PYTHONPATH" && \
	py.test --no-cov tests/specification_tests

tox:
	tox --parallel auto

#-----------------------------------------------------------------------
# Rules
#-----------------------------------------------------------------------
clean:
	rm -rf build; \
	rm -rf dist; \
	rm -rf UnleashClient.egg-info;

build-package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*
