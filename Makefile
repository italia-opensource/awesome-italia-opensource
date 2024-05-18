.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup:
	chmod -R +x ./scripts/dev.sh && ./scripts/dev.sh

setup-ci:
	pip3 install -r requirements.txt && pre-commit install

lint:
	pre-commit run --all-files

check-data:
	python3 scripts/check.py

render-data:
	python3 scripts/render.py

test: lint check-data render-data