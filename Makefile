.PHONY: help

help: ## Helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/\n\t/'

.DEFAULT_GOAL := help

setup: ## Setup local environment
	chmod -R +x ./scripts/dev.sh && ./scripts/dev.sh

setup-ci: ## Setup CI environment
	pip3 install -r requirements.txt && pre-commit install

lint: ## Run linter on all files
	pre-commit run --all-files

check-data: ## Validate awesome data with jsonschema
	python3 scripts/check.py

process-data: ## Genereta anayltics from awesome data
	python3 scripts/process.py $(ARGS)

render-data: ## Render awesome data to README.md
	python3 scripts/render.py

test: lint check-data render-data ## Run all tests

release: check-data process-data render-data ## Release