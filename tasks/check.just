check:
    poetry run pytest -q

lint:
    poetry run python -m compileall src tests

coverage:
    poetry run pytest --cov=src --cov-report=term-missing tests
