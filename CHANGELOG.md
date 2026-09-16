# Changelog

Public workflow changes are recorded here before each release.

## Unreleased

### Added

- Real scikit-learn training, cross-validation and permutation importance.
- Validated YAML/JSON configurations and configuration-only CLI validation.
- Immutable registry snapshots, artifact integrity checks, quality gates and
  sequential rollback history, with local writer locking and atomic metadata.
- Prediction, readiness and liveness endpoints with request validation.
- End-to-end tests, Linux/Windows CI, installed-wheel checks and container tests.
- Contribution, security, configuration, architecture and release guides.

### Changed

- Runtime dependencies replace local pandas/FastAPI substitutes.
- Model selection now fits the requested estimator instead of always returning
  the majority-class baseline. PyTorch is an optional extra.
- Local tracking records configuration, metrics and outcomes per run; the
  misleading placeholder MLflow service has been removed.
- One Dockerfile provides locked, non-root training and serving targets.
- Task commands use the same formatter, linter and type checker as CI.

### Migration

Retrain models produced before this change. Artifacts now include a feature
schema and are stored under `artifacts/models/<name>/v<version>.pkl`.
Evaluation/inference configurations can select a registry name/version or alias.
The old unversioned `artifacts/baseline_model.pkl` path is no longer written.
Use `docker build --target train` or `--target serve` from the root Dockerfile.
