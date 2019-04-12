SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = UnleashClient

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------
test: lint pytest

precommit: clean generate-requirements

build: clean build-package upload

build-local: clean build-package

#-----------------------------------------------------------------------
# Install
#-----------------------------------------------------------------------

install:
	pip install -r requirements.txt

update:
	pip install -U -r requirements-dev.txt && \
	pip install -U -r requirements-package.txt && \
	pip freeze > requirements.txt;

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------
lint:
	pylint ${PROJECT_NAME} && \
	mypy ${PROJECT_NAME};

pytest:
	export PYTHONPATH=${ROOT_DIR}: $$PYTHONPATH && \
	py.test --cov ${PROJECT_NAME} tests/unit_tests


#-----------------------------------------------------------------------
# Rules
#-----------------------------------------------------------------------
clean:
	rm -rf build; \
	rm -rf dist;

build-package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*
