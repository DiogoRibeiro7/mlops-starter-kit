.PHONY: install check lint format test train evaluate serve schema data docs docs-serve

install:
	poetry sync

check:
	poetry check --lock
	poetry run python scripts/check.py

lint:
	poetry run flake8 src tests scripts
	poetry run mypy

format:
	poetry run black src tests scripts

test:
	poetry run pytest --cov --cov-report=term-missing

train:
	poetry run mlops-starter-kit confs/training.yaml

evaluate:
	poetry run mlops-starter-kit confs/evaluations.yaml

schema:
	poetry run mlops-starter-kit --schema

serve:
	poetry run uvicorn mlops_starter_kit.api:app --host 127.0.0.1 --port 8000

docs:
	poetry run mkdocs build --strict

docs-serve:
	poetry run mkdocs serve

data:
	poetry run python -m mlops_starter_kit.data data/raw/example.csv data/processed/example.csv
