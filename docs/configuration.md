# Configuration

Jobs consume YAML or JSON mappings. YAML is parsed with `yaml.safe_load` and
then validated with Pydantic. Unknown keys and invalid values fail before job
execution. Relative paths are resolved against the working directory, so run
the checked-in examples from the repository root. Use absolute paths when
launching jobs elsewhere.

```bash
poetry run mlops-starter-kit confs/training.yaml --validate
poetry run mlops-starter-kit --schema
```

`--validate` prints the configuration including defaults without creating
artifacts. `--schema` returns JSON schemas for all jobs. Errors go to stderr,
results to stdout as structured JSON; failures return a nonzero status.
`--debug` retains Python tracebacks for diagnosis.

## Training

```yaml
job:
  kind: training
dataset:
  path: data/raw/example.csv
  target_column: target
  test_size: 0.2
  random_seed: 42
model:
  name: example
  algorithm: random_forest
  parameters:
    n_estimators: 100
    max_depth: 4
artifacts:
  directory: artifacts
  registry: artifacts/registry.json
tracking:
  directory: artifacts/tracking
```

Algorithms are `baseline_model`, `logistic_regression` and `random_forest`.
The model name is a registry identifier, independent of its algorithm. Names
must start with a letter or digit and contain only letters, digits, `_`, `.`
or `-`, up to 64 characters. Estimator parameters are checked by scikit-learn.

## Model Selection

Evaluation, inference and explanation accept a `model` mapping:

```yaml
model:
  registry: artifacts/registry.json
  name: baseline_model
  version: 1
```

Omit `version` for the latest version, or select `alias: champion` instead.
An alias determines both the model name and version. A trusted local `path`
can be used instead of registry selection; it cannot be combined with a
version or alias. Registry-backed reads verify SHA-256 before loading.

## Tracking and Environment

Every job writes a unique JSON run record with its configuration, timestamps,
status and metrics. Failed jobs include their error. Configurations and errors
can contain sensitive values, so keep secrets out of job configurations.

The service reads `MODEL_PATH` on startup. It does not load `.env` automatically;
export the variable in the shell or pass it to Docker. The legacy `config.py`
helpers continue to support earlier environment-based scripts.
