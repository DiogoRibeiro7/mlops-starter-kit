├── .dev/                       # Devcontainer & editor settings
│   ├── devcontainer.json       # VSCode DevContainer config
│   └── vscode/
│       └── settings.json       # Editor settings (linting, formatting)
├── docker/                     # Dockerfiles and build contexts
│   ├── base.Dockerfile         # Base image
│   ├── train.Dockerfile        # Training environment
│   └── serve.Dockerfile        # Model serving image
├── src/                        # Your Python package
│   ├── mlops_starter_kit/      # Package code
│   │   ├── __init__.py         # Package init
│   │   ├── config.py           # Configuration variables
│   │   ├── data.py             # Data ingest/download logic
│   │   ├── features.py         # Feature engineering
│   │   ├── modeling/           # Training & inference
│   │   │   ├── __init__.py
│   │   │   ├── train.py        # Training pipeline
│   │   │   └── predict.py      # Inference logic
│   │   └── plots.py            # Visualization helpers
│   └── scripts/                # CLI entry-points (fire, click)
├── data/                       # Data lifecycle directories
│   ├── raw/                    # Immutable source dumps
│   ├── external/               # Third-party data
│   ├── interim/                # Cleaned & transformed
│   └── processed/              # Final tables for modeling
├── mlops/                      # Pipelines & orchestration APIs
│   ├── airflow/                # Airflow DAGs & plugins
│   ├── kubeflow/               # Kubeflow Pipelines
│   └── utils/                  # Shared pipeline utilities
├── tests/                      # pytest tests (mirrors `src/`)
│   ├── unit/                   # Unit tests for modules
│   └── integration/            # End-to-end pipeline tests
├── scripts/                    # One-off helper scripts & utilities
├── submodules/                 # Git submodules (shared code)
├── .github/                    # CI/CD workflows & templates
│   └── workflows/
├── docs/                       # Project documentation
│   └── structure.md            # File tree and project layout description
├── Makefile                    # `make data`, `make train`, `make test`, …
├── requirements.txt            # Pinned dependencies
├── setup.cfg                   # flake8, isort, mypy configs
├── pyproject.toml              # Packaging + black config
├── README.md                   # Project overview & quickstart
└── LICENSE                     # Open-source license
