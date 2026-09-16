check:
    poetry check --lock
    poetry run python scripts/check.py

lint:
    poetry run flake8 src tests scripts
    poetry run mypy

coverage:
    poetry run pytest --cov --cov-report=term-missing
