# -*- coding: utf-8 -*-

# This file is part of thumbor-wand-engine
# https://github.com/scorphus/thumbor-wand-engine

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2020-2021, Pablo S. Blum de Aguiar <scorphus@gmail.com>

SHELL=/bin/bash  # helps with the glob below

# Ignore tests that do not include the engine in any way
IGNORE_TESTS := --ignore-glob=*test_{autojpg,format,max_age}.py

# list all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
.PHONY: list
# required for list
no_targets__:

# install dependencies and pre-commit hooks
setup:
	@PIP_REQUIRE_VIRTUALENV=true pip install -U -e .[tests]
	@pre-commit install -f --hook-type pre-commit
	@pre-commit install -f --hook-type pre-push
	@git submodule update --init --recursive
	@PIP_REQUIRE_VIRTUALENV=true pip install -U -e thumbor[tests]
.PHONY: setup

# install dependencies
setup-ci:
	@pip install -U -e .[tests]
	@pip install -U -e thumbor[tests]
.PHONY: setup-ci

# run isort, black and flake8 for style guide enforcement
isort:
	@isort .
.PHONY: isort

black:
	@black --config ./pyproject.toml .
.PHONY: black

flake8:
	@flake8
.PHONY: flake8

lint: isort black flake8
.PHONY: lint

# clean python object, test and coverage files
pyclean:
	@find . -type d -iname '__pycache__' -exec rm -rf \{\} + -print
	@find . -type d -iname '.benchmarks' -exec rm -rf \{\} + -print
	@find . -type d -iname '.mypy_cache' -exec rm -rf \{\} + -print
	@find . -type d -iname '.pytest_cache' -exec rm -rf \{\} + -print
	@find . -type d -iname '*.egg-info' -exec rm -rf \{\} + -print
	@find . -type f -iname '.coverage' -exec rm -rf \{\} + -print
	@find . -type f -name "*.pyc" -delete -print
.PHONY: pyclean

compile_ext:
	@cd thumbor && $(MAKE) compile_ext
.PHONY: compile_ext

unit:
	@pytest -sv --cov=thumbor_wand_engine tests/
.PHONY: unit

integration:
	@pytest -sv --cov=thumbor_wand_engine integration_tests/
.PHONY: integration

acceptance:
	@env ENGINE=thumbor_wand_engine pytest -sv --cov=thumbor_wand_engine \
		thumbor_tests/filters/ $(IGNORE_TESTS)
.PHONY: acceptance

coverage-html:
	@coverage html
.PHONY: coverage-html

test: unit
.PHONY: test

test-ci:
	@if [ -n "$$ACCEPTANCE_TEST" ]; then \
		$(MAKE) compile_ext acceptance; \
	elif [ -n "$$LINT_TEST" ]; then \
		$(MAKE) lint; \
	elif [ -n "$$INTEGRATION_TEST" ]; then \
		$(MAKE) integration; \
	elif [ -n "$$UNIT_TEST" ]; then \
		$(MAKE) unit; \
	else \
		echo "I don't know what to do ¯\_(ツ)_/¯"; \
		exit 1; \
	fi
.PHONY: test-ci
