.PHONY: setup lint format typecheck test cover ci clean

setup: ## Create venv, install deps + package (editable)
	uv sync

lint: ## Ruff check + formatting gate
	uv run ruff check src tests
	uv run ruff format --check src tests

format: ## Auto-format
	uv run ruff format src tests
	uv run ruff check --fix src tests

typecheck: ## Mypy strict
	uv run mypy

test: ## Fast test run
	uv run pytest

cover: ## Tests with coverage gate (fail_under=95)
	uv run pytest --cov --cov-report=term-missing

ci: lint typecheck cover ## Full local CI equivalent
	@echo "CI gates green"

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov dist
