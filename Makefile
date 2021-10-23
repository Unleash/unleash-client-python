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

install-clean:
	pip install -U -r requirements-dev.txt && \
	pip install -U -r requirements-package.txt

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------
lint:
	pylint ${PROJECT_NAME} && \
	mypy ${PROJECT_NAME} --install-types --non-interactive;

pytest:
	export PYTHONPATH="${ROOT_DIR}:$$PYTHONPATH" && \
	py.test --flake8 --cov ${PROJECT_NAME} tests/unit_tests

specification-test:
	export PYTHONPATH="${ROOT_DIR}:$$PYTHONPATH" && \
	py.test tests/specification_tests

tox-osx:
	tox -c tox-osx.ini --parallel auto

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
