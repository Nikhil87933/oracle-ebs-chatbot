.PHONY: install format lint lint-fix check-format typecheck test coverage check fix clean

install:
	pip install -e ".[dev]"
	pre-commit install

format:
	black .

lint:
	ruff check .

lint-fix:
	ruff check . --fix

check-format:
	black --check .

typecheck:
	mypy src

test:
	pytest

coverage:
	pytest --cov=src --cov-report=html

check: lint check-format typecheck test

fix: format lint-fix

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
