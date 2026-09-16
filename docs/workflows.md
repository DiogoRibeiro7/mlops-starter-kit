# Workflow Guide

## Train and Compare

Run the examples from the repository root after `poetry sync`:

```bash
poetry run mlops-starter-kit confs/training.yaml
poetry run mlops-starter-kit confs/tuning.yaml
poetry run mlops-starter-kit confs/evaluations.yaml
poetry run mlops-starter-kit confs/explanations.yaml
```

Training registers `baseline_model`; tuning registers `tuned_model`. The
registry names describe example versions, while each config's `algorithm`
chooses the estimator. Tuning requires at least `search.folds` training rows
per class. Its `cv_accuracy` and held-out metrics are reported separately.

The evaluation and explanation examples read the included fixture. For a real
project, point them to an independent labelled dataset. Permutation importance
measures loss of accuracy when a feature is shuffled; a zero importance for a
constant baseline is expected.

## Promote and Roll Back

`confs/promotion.yaml` promotes version 1 only when its stored held-out accuracy
is at least 0.75. Set the threshold according to your domain, not the synthetic
fixture's score.

```bash
poetry run mlops-starter-kit confs/promotion.yaml
```

Train another version, change `model.version` in the promotion configuration
to that version and promote it. Then `confs/rollback.yaml` restores the prior
target with an audit reason. Repeated rollbacks walk backwards through prior
promotions and fail when no earlier target remains. A missing or modified
artifact cannot be promoted or restored.

## Batch Inference

`confs/inference.yaml` writes `artifacts/predictions.csv`. Its input may contain
the original target column, which is removed before prediction. All trained
feature columns must be present; unexpected columns are rejected. Feature order
is restored from the artifact. No output file is written if validation fails.

## Service Deployment

Set `MODEL_PATH` to a trusted versioned artifact and run the API as described
in the README. `/healthz` checks process liveness; `/readyz` checks model
availability. `/predict` returns 422 for invalid records and 503 without a model.

Use the same dependencies for training and serving, mount artifacts read-only,
and configure authentication, TLS and limits in a gateway. Neither the local
API nor registry is a complete multi-tenant deployment platform.
