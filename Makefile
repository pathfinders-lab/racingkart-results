.PHONY: install test lint format build

install:
	uv sync

test:
	PYTHONPATH="" uv run pytest tests/ -v

lint:
	uv run ruff check render/ tests/

format:
	uv run ruff format render/ tests/

build:
	uv run python render/build_site.py
