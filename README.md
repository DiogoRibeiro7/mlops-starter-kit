# mlops-starter-kit

A minimal skeleton for starting MLOps projects.
Currently this repository only includes:

- **Devcontainer** configuration for consistent development environments
- **Dockerfiles** for training and serving images
- **A basic** `Makefile` with placeholder commands
- **Example** configuration in `config.py`

Additional modules and CI workflows can be added as your project grows.

## Setup

This project manages dependencies with [Poetry](https://python-poetry.org/).
Install Poetry and use it to create the virtual environment from
`pyproject.toml`:

```bash
pip install poetry
poetry install
make dev  # launch and connect to devcontainer
```

## Quickstart

This repository does not yet include a full pipeline. You can still build the
provided Docker images to experiment with the environment:

```bash
# Build the training image
docker build -f docker/train.Dockerfile -t mlops-starter-kit:train .

# Build the serving image and run it locally
docker build -f docker/serve.Dockerfile -t mlops-starter-kit:serve .
docker run -p 8000:8000 mlops-starter-kit:serve
```
