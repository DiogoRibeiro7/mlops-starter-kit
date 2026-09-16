# MLOps Starter Kit

[![CI](https://github.com/DiogoRibeiro7/mlops-starter-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/DiogoRibeiro7/mlops-starter-kit/actions/workflows/ci.yml)

A reusable Python template for numeric classification projects: validated
configuration, reproducible training, model versioning, batch inference and
a FastAPI prediction service.

**Python 3.10-3.14 | Poetry 2.2.1 | MIT license**

## Quickstart

From a clone of this repository:

```bash
python -m pip install poetry==2.2.1
poetry sync
poetry run mlops-starter-kit confs/training.yaml
poetry run mlops-starter-kit confs/evaluations.yaml
poetry run mlops-starter-kit confs/inference.yaml
```

Training uses the included [synthetic dataset](data/README.md), evaluates a
logistic regression on a held-out split, and creates:

- An immutable model under `artifacts/models/baseline_model/v1.pkl`.
- A registry entry containing metrics and model/data SHA-256 fingerprints.
- A run record and resolved configuration under `artifacts/`.

Each subsequent training run creates a new version. The example scores are
a workflow check, not evidence of performance on real data.

## Workflows

| Command | Result |
| --- | --- |
| `mlops-starter-kit confs/training.yaml` | Train and register a version |
| `mlops-starter-kit confs/tuning.yaml` | Cross-validate a parameter grid, evaluate the winner and register it |
| `mlops-starter-kit confs/evaluations.yaml` | Evaluate a registered version on a labelled CSV |
| `mlops-starter-kit confs/inference.yaml` | Write schema-checked predictions to CSV |
| `mlops-starter-kit confs/explanations.yaml` | Write permutation feature importance |
| `mlops-starter-kit confs/promotion.yaml` | Promote a version meeting an accuracy threshold |
| `mlops-starter-kit confs/rollback.yaml` | Restore the previous promoted version |

Prefix these commands with `poetry run`. Rollback requires two different
versions to have been promoted. See the [workflow guide](docs/workflows.md)
for model selection, promotion and serving.

## Prediction API

After training, set the model path and start the server:

```bash
export MODEL_PATH=artifacts/models/baseline_model/v1.pkl
poetry run uvicorn mlops_starter_kit.api:app --host 127.0.0.1 --port 8000
```

In PowerShell, use
`$env:MODEL_PATH = "artifacts/models/baseline_model/v1.pkl"`.

The API exposes `/healthz`, `/readyz`, `/predict` and OpenAPI docs at `/docs`.
Without a model, liveness succeeds and readiness/prediction return HTTP 503.

```bash
curl http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"instances":[{"feature1":1,"feature2":1}]}'
```

## Development

```bash
poetry run python scripts/check.py
poetry run pre-commit install
```

The check command runs formatting, lint, typing and tests with a minimum
85% branch-aware coverage requirement. `make check` and `just check` run the
same checks. CI also tests the built wheel and both Docker targets.

Validate configuration without executing a job:

```bash
poetry run mlops-starter-kit confs/training.yaml --validate
poetry run mlops-starter-kit --schema
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution process.

## Docker

```bash
docker build --target train -t mlops-starter-kit:train .
docker build --target serve -t mlops-starter-kit:serve .
docker volume create model-artifacts
docker run --rm -v model-artifacts:/app/artifacts mlops-starter-kit:train
docker run --rm -p 8000:8000 \
  -v model-artifacts:/app/artifacts:ro \
  -e MODEL_PATH=/app/artifacts/models/baseline_model/v1.pkl \
  mlops-starter-kit:serve
```

The runtime uses an installed wheel and runs as a non-root user.
PyTorch is an optional `deep-learning` extra:
`poetry install --extras deep-learning`.

## Template Adoption

1. Change the distribution name, import package, author and repository URLs.
2. Replace the synthetic CSV with your data and define the feature contract.
3. Select the model, validation strategy and promotion threshold.
4. Configure deployment authentication, storage and secret management.
5. Run the complete checks and container workflow before your first release.

[Architecture](docs/architecture.md) | [Configuration](docs/configuration.md) |
[Releases](docs/releases.md) | [Roadmap](docs/roadmap.md) | [Security](SECURITY.md)

## Operational Scope

This is a local reference implementation. The registry coordinates writers
on one shared local filesystem; it is not a distributed model registry.
Models use pickle and must come from a trusted source. The API has no built-in
authentication; put authentication and TLS in front of it before exposing it
outside a trusted environment. See [SECURITY.md](SECURITY.md).
