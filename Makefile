.PHONY: dev data train test serve lint schema evaluate clean

dev:
	docker run --rm -it \
	  --mount type=bind,src=$(PWD),dst=/workspace \
	  --workdir /workspace \
	  -v ~/.cache:/home/vscode/.cache \
	  mcr.microsoft.com/vscode/devcontainers/base:ubuntu \
	  /bin/bash

data:
	poetry run python -m mlops_starter_kit.data

train:
	poetry run mlops-starter-kit confs/training.yaml

test:
	poetry run pytest --maxfail=1 --disable-warnings -q

lint:
	pre-commit run --files $(shell git ls-files '*.py')

schema:
	poetry run mlops-starter-kit --schema

evaluate:
	poetry run mlops-starter-kit confs/evaluations.yaml

serve:
	docker build -f docker/serve.Dockerfile -t mlops-starter-kit:serve .
	docker run -p 8000:8000 mlops-starter-kit:serve

clean:
	rm -rf artifacts .pytest_cache htmlcov dist build
