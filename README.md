# MLOps Starter Kit

[![CI](https://github.com/DiogoRibeiro7/mlops-starter-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/DiogoRibeiro7/mlops-starter-kit/actions/workflows/ci.yml)
[![PR Checks](https://github.com/DiogoRibeiro7/mlops-starter-kit/actions/workflows/pr.yml/badge.svg)](https://github.com/DiogoRibeiro7/mlops-starter-kit/actions/workflows/pr.yml)

`mlops-starter-kit` is a package-first template for reproducible machine-learning workflows. It follows the same broad architecture as `mlops-python-package`: installable source code, explicit IO boundaries, config-driven jobs, local model registry primitives, CI checks, Docker entrypoints and maintained architecture documentation.

This repository remains generic. It does not copy the bike-demand dataset or domain-specific implementation from the reference project; instead it provides the same shape for a new MLOps codebase.

## Architecture

The project centers on an installable Python package and CLI:

| Path | Responsibility |
| --- | --- |
| `src/mlops_starter_kit/core/` | Models, metrics and lightweight dataframe schemas |
| `src/mlops_starter_kit/io/` | Configs, datasets, provenance, local registry and service boundaries |
| `src/mlops_starter_kit/jobs/` | Training, tuning, inference, evaluation, explanation, promotion and rollback jobs |
| `src/mlops_starter_kit/utils/` | Search, signature and splitting helpers plus compatibility utilities |
| `confs/` | Example job configurations |
| `tests/` | Unit and integration tests |
| `documentation/` | Architecture notes and roadmap |
| `tasks/` | `just` task fragments for local automation |

See [`documentation/ARCHITECTURE.md`](documentation/ARCHITECTURE.md) for the component view and intentional limits.

## Development Setup

Install Poetry and create the environment from `pyproject.toml`:

```bash
pip install poetry
poetry install
```

Run the same core checks used by CI:

```bash
make lint
make test
```

If you use `just`, the task layout mirrors the reference project:

```bash
just --list
just check
just train
```

## Quickstart

Run the starter training job against the small example dataset:

```bash
poetry run mlops-starter-kit confs/training.yaml
```

That command loads `data/raw/example.csv`, validates the target column, trains a majority-class baseline, writes a model artifact under `artifacts/`, fingerprints the training data and registers the model in a local JSON registry.

After training, evaluate the saved model:

```bash
poetry run mlops-starter-kit confs/evaluations.yaml
```

Inspect the CLI schema:

```bash
poetry run mlops-starter-kit --schema
```

## Docker

Build and run the serving image locally:

```bash
docker build -f docker/serve.Dockerfile -t mlops-starter-kit:serve .
docker run -p 8000:8000 mlops-starter-kit:serve
```

## Configuration

Job configs live in `confs/` and use a small YAML subset that works without optional dependencies. The legacy `configs/` directory remains for compatibility with earlier examples.

Environment variables can still be stored in a `.env` file. Key variables include:

```text
PROJECT_NAME
DATASET_PATH
DATASET_FILENAME
TARGET_COL
RAW_DIR
PROCESSED_DIR
ARTIFACTS_DIR
```
