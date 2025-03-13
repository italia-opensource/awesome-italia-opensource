.PHONY: help

help: ## Helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/\n\t/'

.DEFAULT_GOAL := help

.PHONY: doppler
doppler: ## Download secrets from Doppler
	@chmod +x ./scripts/doppler.sh && ./scripts/doppler.sh

.PHONY: setup
setup: doppler ## Setup local environment
	chmod +x ./scripts/setup.sh && ./scripts/setup.sh

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
test: check-data render-data ## Run all tests

.PHONY: release
release: check-data process-data render-data ## Release
