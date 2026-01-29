# Makefile for pdql

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UV := $(VENV)/bin/uv
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy

UV_VERSION := 0.9.27

.PHONY: setup test format lint build publish clean

setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install uv==$(UV_VERSION)
	$(PIP) install -e .[dev]

test:
	PYTHONPATH=src $(PYTEST) tests/

format:
	$(RUFF) format src tests

lint:
	$(FLAKE8) src tests
	$(MYPY) src

build:
	$(UV) build

publish:
	$(UV) publish

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
