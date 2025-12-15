.PHONY: install test lint fmt gen-readme

install:
pip install -e .[dev]

test:
pytest

lint:
ruff check .

fmt:
ruff format .

gen-readme:
python scripts/generate_command_reference.py
