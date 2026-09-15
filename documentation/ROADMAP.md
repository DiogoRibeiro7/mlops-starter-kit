# Roadmap

## Package Architecture

- Keep the package-first structure aligned with `core`, `io`, `jobs` and `utils` ownership boundaries.
- Replace the starter baseline model with project-specific estimators.
- Add typed config models once the project chooses Pydantic, Hydra or OmegaConf as the durable configuration layer.

## Reproducibility

- Pin runtime dependencies with a lockfile.
- Add artifact and dataset fingerprint checks to every job that reads or writes model-ready data.
- Promote model versions only from completed evaluation evidence.

## Validation

- Add schema validation for feature and target tables.
- Add integration tests that run training, evaluation, promotion and rollback outside the source checkout.
- Define acceptance thresholds per model family and dataset.

## Operations

- Replace the local JSON registry with MLflow Model Registry or another managed registry.
- Add remote tracking-store support.
- Build and smoke-test a package image with networking disabled where practical.

## Documentation

- Keep `README.md`, `documentation/ARCHITECTURE.md` and this roadmap aligned with the actual implementation.
- Add generated API documentation once the public package surface stabilizes.
