SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------

build: clean generate-requirements build-package upload

#-----------------------------------------------------------------------
# Rules
#-----------------------------------------------------------------------
clean:
	rm -rf build; \
	rm -rf dist;

generate-requirements:
	pipenv lock -r > requirements.txt; \
	pipenv lock -r --dev >> requirements-dev.txt;

build-package:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*