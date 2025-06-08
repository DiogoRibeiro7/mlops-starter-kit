.PHONY: dev data train test serve

dev:
	docker run --rm -it \
	  --mount type=bind,src=$(PWD),dst=/workspace \
	  --workdir /workspace \
	  -v ~/.cache:/home/vscode/.cache \
	  mcr.microsoft.com/vscode/devcontainers/base:ubuntu \
	  /bin/bash

data:
    python -m src.mlops_starter_kit.data

train:
	python -m src.mlops_starter_kit.modeling.train

test:
	pytest --maxfail=1 --disable-warnings -q

serve:
	docker build -f docker/serve.Dockerfile -t mlops-starter-kit:serve .
	docker run -p 8000:8000 mlops-starter-kit:serve
