NAME = k4
VERSION = $(shell poetry version -s)

SHELL := /bin/bash

.PHONY: help all

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build:  ## Build docker image
	docker build . --tag $(NAME)

build-dev:  ## Build dev docker image
	docker build -f Dockerfile.dev . --tag $(NAME)
	
dev:  ## Run dev container
	kubectl exec -it $(NAME) -c $(NAME) --namespace kafka -- poetry run bash
	
lint:  ## Lint python
	poetry run black --line-length 100 src tests

test:  ## Test python
	poetry run pytest

setup-demo:	 ## Setup Demo
	sh demo/setup.sh

teardown-demo:  ## Teardown Demo
	sh demo/teardown.sh

# coverage: test ## Test python
# 	poetry run coverage report -m
# 	poetry run coverage lcov

release: lint test coverage ## Push tags and trigger Github Actions release.
	git tag $(VERSION)
	git push --tags

clean: ## Remove Python cache files.
	@rm -rf build dist .eggs *.egg-info .venv requirements.txt
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +