# mlops-starter-kit

A production-ready starter kit for building and deploying end-to-end ML pipelines. Includes:

- **Devcontainer** for consistent development environments
- **Dockerfiles** for training & serving images
- **CI/CD** workflows under `.github/workflows`
- **Orchestration** templates for Airflow and Kubeflow
- **Modular code layout** with `src/mlops_starter_kit`

## Setup

```bash
pip install -r requirements.txt
make dev  # launch and connect to devcontainer
```

## Usage

- `make data` to download and preprocess data

- `make train` to train models

- `make serve` to spin up a local API
