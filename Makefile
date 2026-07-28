.PHONY: help install test lint run benchmark clean

help:
	@echo "Available commands:"
	@echo "  make install    Install package in editable mode"
	@echo "  make test       Run pytest test suite"
	@echo "  make lint       Run ruff & black code quality checks"
	@echo "  make run        Run Version 1 baseline pipeline"
	@echo "  make clean      Remove build and cache artifacts"

install:
	pip install -e .[dev]

test:
	pytest tests/ -v

lint:
	ruff check cell_tracking/ tests/
	black --check cell_tracking/ tests/

run:
	python scripts/run_pipeline.py --config configs/baseline.yaml

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
