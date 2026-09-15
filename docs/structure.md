# Project Structure

The repository now follows a package-first MLOps layout with config-driven jobs.

```
.
├── .dev/               # Devcontainer & editor settings
│   ├── devcontainer.json
│   └── vscode/
│       └── settings.json
├── confs/              # Job configuration files
├── docker/             # Dockerfiles and build contexts
│   ├── base.Dockerfile
│   ├── train.Dockerfile
│   └── serve.Dockerfile
├── documentation/      # Maintained architecture and roadmap docs
├── docs/               # Legacy documentation entrypoints
│   └── structure.md    # This file
├── data/               # Raw and processed datasets
│   └── raw/example.csv
├── scripts/            # Helper CLI scripts
│   ├── ingest_data.py
│   └── serve_model.sh
├── notebooks/          # Example notebooks
│   └── example_pipeline.ipynb
├── src/                # Python source code
│   └── mlops_starter_kit/
│       ├── core/       # Models, metrics and schemas
│       ├── io/         # Configs, datasets, provenance and registry
│       ├── jobs/       # Training, inference, evaluation and governance jobs
│       └── utils/      # Search, split and signature helpers
├── tasks/              # just task fragments
├── tests/              # Unit and integration tests
├── justfile            # just automation entrypoint
├── Makefile            # Helper targets
├── README.md           # Project overview
└── LICENSE             # License information
```

These directories separate domain logic from IO, executable workflows and local
automation so the starter can grow into a real package without a large rewrite.
