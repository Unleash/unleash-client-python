SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = UnleashClient

.PHONY: sphinx

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------
test: lint pytest specification-test

precommit: clean generate-requirements

build: clean build-package upload

build-local: clean build-package

docs: docker-docs-stop sphinx docker-docs

#-----------------------------------------------------------------------
# Install
#-----------------------------------------------------------------------

install:
	pip install -U -r requirements.txt && \
	pip install . && \
	./scripts/get-spec.sh

install-docs: install
	pip install -U -r requirements-docs.txt

#-----------------------------------------------------------------------
# Testing & Linting
#-----------------------------------------------------------------------
fmt:
	black . && \
	ruff UnleashClient tests --fix

lint:
	black . --check && \
	ruff UnleashClient tests docs && \
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
	python -m build

upload:
	twine upload dist/*

#-----------------------------------------------------------------------
# Docs
#-----------------------------------------------------------------------
docker-docs-stop:
	docker stop unleash-docs | true

sphinx:
	cd docs; \
	rm -rf _build; \
	make html;

docker-docs:
	docker run -d --name unleash-docs --rm -v `pwd`/docs/_build/html:/web -p 8080:8080 halverneus/static-file-server:latest
