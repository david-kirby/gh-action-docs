.PHONY: tests

build: clean
	@echo "Building package"
	@poetry build

deps:
	@echo "Installing deps"
	@poetry install

deps-prod:
	@echo "Installing deps"
	@poetry install --no-root --no-dev

clean:
	@echo "Cleaning build artifacts"
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .benchmarks .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

tests:
	@echo "Running tests"
	@poetry run python -m unittest

lint:
	@echo "Linting"
	@poetry run black src/* tests/*
	@poetry run flake8 src/* tests/*

poetry:
	@echo "Install poetry"
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -