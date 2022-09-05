.PHONY: help

help: ## helper
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.DEFAULT_GOAL := help

setup:
	chmod -R +x ./setup.sh && ./setup.sh

setup-ci:
	pip3 install -r requirements.txt

lint:
	pre-commit run --all-files && python3 cli.py

lint-ci:
	python3 cli.py && make lint

render:
	python3 cli.py --render --output
