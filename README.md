# mlops-starter-kit

A production-ready starter kit for building and deploying end-to-end ML pipelines. Includes:

- **Devcontainer** for consistent development environments
- **Dockerfiles** for training & serving images
- **CI/CD** workflows under `.github/workflows`
- **Orchestration** templates for Airflow and Kubeflow
- **Modular code layout** with `src/mlops_starter_kit` (skeleton only)

## Setup

```bash
pip install -r requirements.txt
make dev  # launch and connect to devcontainer
```

## Quickstart (CPU)

```bash
make data   # download and preprocess data
make train  # train models (CPU)
make serve  # build & run serving container at localhost:8000 (CPU)
```

## Quickstart (GPU)

If you have NVIDIA GPUs and the NVIDIA Container Toolkit installed, you can build and run GPU-enabled images:

```bash
# Build GPU training image
docker build -f docker/train.Dockerfile -t mlops-starter-kit:train-gpu .
# Run training with GPU
docker run --gpus all mlops-starter-kit:train-gpu

# Build GPU serving image
docker build -f docker/serve.Dockerfile -t mlops-starter-kit:serve-gpu .
# Run serving with GPU
docker run --gpus all -p 8000:8000 mlops-starter-kit:serve-gpu
```
