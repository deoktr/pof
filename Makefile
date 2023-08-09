.PHONY: virtualenv requirements format

PYTHON ?= python3.10
VENV ?= ./venv
ENV_PYTHON ?= $(VENV)/bin/python


virtualenv:
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		$(VENV)/bin/pip install pip; \
	fi

requirements: virtualenv
	$(VENV)/bin/pip install -r requirements.txt
	$(VENV)/bin/pip install -r requirements.dev.txt

install-pre-commit:
	$(PYTHON) -m pip install --upgrade pre-commit
	pre-commit install

pre-commit:
	pre-commit run --all-file

dev: install-pre-commit requirements
	@echo
	@echo 'done setting dev environment'
	@echo 'run `source ./venv/bin/activate`'
	@echo

test: virtualenv
	$(ENV_PYTHON) -m pytest

coverage: test
	$(ENV_PYTHON) -m coverage html

format: virtualenv
	$(PYTHON) -m black .
	$(PYTHON) -m ruff .
