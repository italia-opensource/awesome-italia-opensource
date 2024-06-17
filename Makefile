.PHONY: help

help: ## Helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/\n\t/'

.DEFAULT_GOAL := help
VIRTUAL_ENV := true

.PHONY: doppler
doppler: ## Install deps
	@chmod +x ./scripts/doppler.sh && ./scripts/doppler.sh

.PHONY: deps
deps: ## Setup local environment
	chmod +x ./scripts/deps.sh && ./scripts/deps.sh $(VIRTUAL_ENV)

.PHONY: setup
setup: doppler deps ## Setup local environment

.PHONY: setup-ci
setup-ci: ## Setup CI environment
	pip3 install -r requirements.txt && pre-commit install

.PHONY: lint
lint: ## Run linter on all files
	pre-commit run --all-files

.PHONY: check-data
check-data: ## Validate awesome data with jsonschema
	python3 scripts/check.py

.PHONY: process-data
process-data: ## Genereta anayltics from awesome data
	python3 scripts/process.py $(ARGS)

.PHONY: render-data
render-data: ## Render awesome data to README.md
	python3 scripts/render.py

.PHONY: test
test: lint check-data render-data ## Run all tests

.PHONY: release
release: check-data process-data render-data ## Release
