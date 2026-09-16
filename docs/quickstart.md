# Quickstart

## Install

Use Python 3.10-3.14 and run these commands from a clone of the repository:

```bash
git clone https://github.com/DiogoRibeiro7/mlops-starter-kit.git
cd mlops-starter-kit
python -m pip install poetry==2.2.1
poetry sync
```

The default environment contains the application and development tools.
Documentation dependencies are [optional](documentation.md#local-preview).

## Train and Predict

```bash
poetry run mlops-starter-kit confs/training.yaml
poetry run mlops-starter-kit confs/evaluations.yaml
poetry run mlops-starter-kit confs/inference.yaml
```

The training configuration fits logistic regression on the
[synthetic dataset](dataset.md). It uses `baseline_model` as the registry name;
that name is independent of the estimator. The first run writes:

| Output | Location |
| --- | --- |
| Versioned model | `artifacts/models/baseline_model/v1.pkl` |
| Model registry | `artifacts/registry.json` |
| Training artifacts | `artifacts/runs/` |
| Job records | `artifacts/tracking/` |
| Batch predictions | `artifacts/predictions.csv` |

Each training run creates a new version. The example evaluation reuses the
synthetic table; use a separate labelled dataset for real evaluation.

## Validate Configuration

```bash
poetry run mlops-starter-kit confs/training.yaml --validate
poetry run mlops-starter-kit --schema
```

Validation does not execute a job or write artifacts. See
[configuration](configuration.md) for supported algorithms, paths and model
selection, and [workflows](workflows.md) for tuning, promotion and rollback.

## Adopt the Template

1. Update the package name, import package, author and repository URLs.
2. Replace the fixture with your data and define the feature contract.
3. Choose a validation strategy and promotion thresholds for your domain.
4. Configure authentication, artifact storage and secret handling for deployment.
5. Run the [development checks](contributing.md#changes) before release.

To serve the trained model, continue with the [prediction API](serving.md).
