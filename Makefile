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
.PHONY: setup

# install dependencies
setup-ci:
	@pip install -U -e .[tests]
.PHONY: setup-ci

# run isort, black and flake8 for style guide enforcement
isort:
	@isort .
.PHONY: isort

black:
	@black .
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

unit:
	@pytest -sv --cov=imagemagick_engine tests/
.PHONY: unit

coverage-html:
	@coverage html
.PHONY: coverage-html

test: unit
.PHONY: test
