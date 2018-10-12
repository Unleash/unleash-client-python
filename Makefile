SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

#-----------------------------------------------------------------------
# Rules of Rules : Grouped rules that _doathing_
#-----------------------------------------------------------------------

build: clean build-package upload

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