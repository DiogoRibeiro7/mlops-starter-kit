# Roadmap

The maintained roadmap now lives at [`documentation/ROADMAP.md`](documentation/ROADMAP.md).
This file remains as a compatibility pointer for older links.

---

# Legacy Roadmap

This roadmap outlines enhancements to transform the minimal skeleton into a more production-ready MLOps project template. Iterate on sections or add new ones as needed.

---

## 1. Project Structure & Configuration

Below is a scaffold for the project layout along with example configuration files for environment management, secret handling, and runtime configs.

```bash
├── README.md
├── ROADMAP.md
├── pyproject.toml          # Poetry config
├── environment.yml          # (optional) Conda env
├── .env.example            # Sample env vars
├── configs/
│   ├── config.yaml         # Hydra config
│   └── logging.yaml        # Logging config
├── src/
│   └── mlops_starter_kit/
│       ├── __init__.py
│       ├── main.py         # Entrypoint
│       ├── config.py       # Config loader
│       └── utils.py        # Utility functions
├── tests/
│   ├── test_config.py
│   └── test_utils.py
├── notebooks/
│   └── exploration.ipynb
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── scripts/
    ├── ingest_data.py
    └── serve_model.sh
```

- **Standardize Layout**: Adopt a layered structure (`src/`, `tests/`, `notebooks/`, `configs/`, `docker/`, `scripts/`).
- **Configuration Management**: Integrate [Hydra](https://hydra.cc/) or [OmegaConf](https://omegaconf.readthedocs.io/) for flexible, hierarchical runtime configs.
- **Environment Management**: Use `pyproject.toml` with Poetry for reproducible installs (optionally provide `environment.yml` for Conda users).
- **Secrets Handling**: Support `.env` files and integration with Vault or AWS Secrets Manager.

## 2. Development Workflow

- **Pre-commit Hooks**: Configure `pre-commit` for linting (Flake8), formatting (Black), and type-checking (Mypy).
- **IDE Integration**: Enhance Devcontainer settings with recommended extensions (e.g., Python, Pylance, GitLens).
- **Makefile Targets**: Define `make lint`, `make test`, `make train`, `make serve`, and `make clean`.

## 3. Continuous Integration & Delivery

- **CI Pipelines**: Expand GitHub Actions with workflows for:
  - **Lint & Test** on pull requests.
  - **Build & Push** Docker images on `main`.
  - **End-to-End** smoke tests against a live container.
- **CD Workflow**: Optional templates for deployment to Kubernetes or ECS via Helm or Terraform.

## 4. Data Management

- **Data Versioning**: Integrate DVC or MLflow for dataset and artifact tracking.
- **Ingestion Scripts**: Provide `scripts/ingest_data.py` with parameterized paths.
- **Schema Validation**: Use `great_expectations` for defining and validating data schemas.

## 5. Modeling & Training

- **Modular Code**: Organize `src/mlops_starter_kit/modeling/` into data, features, model, and training modules.
- **Experiment Tracking**: Integrate MLflow or Weights & Biases for logging metrics, parameters, and artifacts.
- **Hyperparameter Tuning**: Include sample workflows with Optuna or Ray Tune.

## 6. Testing & Quality Assurance

- **Unit Tests**: Add `tests/` with pytest fixtures for data and model modules.
- **Integration Tests**: Spin up Docker containers via a test harness and validate endpoints.
- **Coverage Reports**: Generate coverage reports and upload to Codecov or Coveralls.

## 7. Deployment & Serving

- **API Framework**: Template using FastAPI or Flask with auto-generated Swagger docs.
- **Health Checks & Metrics**: Expose `/health` and integrate Prometheus client for custom metrics.
- **Load Testing**: Include sample Locust or JMeter scripts.

## 8. Monitoring & Observability

- **Logging**: Configure structured logging (e.g., JSON) via `structlog` or `loguru`.
- **Tracing**: Instrument with OpenTelemetry for distributed tracing.
- **Alerts**: Integrate with PagerDuty, Slack, or other alerting platforms.

## 9. Documentation & Examples

- **Docs Site**: Scaffold MkDocs or Sphinx site with reference, tutorials, and API docs.
- **README Enhancements**: Expand Quickstart with a real pipeline example.
- **Notebooks**: Add Jupyter notebooks for data exploration and model training demos.

## 10. Advanced Topics (Optional)

- **Feature Store**: Outline integration with Feast.
- **Pipeline Orchestration**: Provide templates for Airflow, Prefect, or Kubeflow.
- **Model Governance**: Add policy checks and bias/fairness reporting.

---

*Next Steps*: Provide feedback on priority areas or additional modules, then scaffold specific code and configs accordingly.
