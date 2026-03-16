PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
APP := $(VENV)/bin/pdf-interpreter

.PHONY: install lint format test train clean

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

test:
	$(PYTEST)

train:
	$(APP) train --config configs/base.yaml

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache
