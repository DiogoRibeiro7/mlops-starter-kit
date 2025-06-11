# mlops-starter-kit

[![CI](https://github.com/your-org/mlops-starter-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/mlops-starter-kit/actions/workflows/ci.yml)
[![PR Checks](https://github.com/your-org/mlops-starter-kit/actions/workflows/pr.yml/badge.svg)](https://github.com/your-org/mlops-starter-kit/actions/workflows/pr.yml)

A minimal skeleton for starting MLOps projects.
Currently this repository only includes:

- **Devcontainer** configuration for consistent development environments
- **Dockerfiles** for training and serving images
- **A basic** `Makefile` with placeholder commands
- **Example** configuration in `config.py`

Additional modules and CI workflows can be added as your project grows.

For planned enhancements see [ROADMAP.md](ROADMAP.md).

## Setup

This project manages dependencies with [Poetry](https://python-poetry.org/).
Install Poetry and use it to create the virtual environment from
`pyproject.toml`:

```bash
pip install poetry
poetry install
make dev  # launch and connect to devcontainer
```

### Running in VS Code

The repository contains a pre-configured devcontainer. From VS Code you can
"Reopen in Container" to get an environment with all dependencies installed.
Alternatively run `make dev` from the command line which uses the same Docker
image.

To format, lint and type-check the codebase locally, run:

```bash
make lint
make test
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

### Example pipeline

An example dataset is provided under `data/raw/example.csv`. A short notebook
(`notebooks/example_pipeline.ipynb`) demonstrates loading this data, training a
model and evaluating it using the utilities in `src/mlops_starter_kit/`.

## Data directories

Raw data files are expected under `data/raw/` and processed data under
`data/processed/` at the project root. You can override these paths by setting
the `RAW_DIR` and `PROCESSED_DIR` environment variables.

Environment variables can be stored in a `.env` file. See `.env.example` for a
list of supported variables used by the configuration loader. Key variables
include:

```
PROJECT_NAME   # overrides the project name
DATASET_PATH   # path where datasets are stored
DATASET_FILENAME  # CSV filename inside DATASET_PATH
TARGET_COL     # name of the target column in the dataset
```
