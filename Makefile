.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup:
	chmod -R +x ./scripts/dev.sh && ./dev.sh

setup-ci:
	pip3 install -r requirements.txt

lint:
	pre-commit run --all-files
