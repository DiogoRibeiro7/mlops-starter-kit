# Project Structure

The repository currently contains only the bare essentials required to start an MLOps project.

```
.
├── .dev/               # Devcontainer & editor settings
│   ├── devcontainer.json
│   └── vscode/
│       └── settings.json
├── docker/             # Dockerfiles and build contexts
│   ├── base.Dockerfile
│   ├── train.Dockerfile
│   └── serve.Dockerfile
├── docs/               # Project documentation
│   └── structure.md    # This file
├── config.py           # Example configuration variables
├── data/               # Raw and processed datasets
│   └── raw/example.csv
├── scripts/            # Helper CLI scripts
│   ├── ingest_data.py
│   └── serve_model.sh
├── notebooks/          # Example notebooks
│   └── example_pipeline.ipynb
├── src/                # Python source code
├── tests/              # Unit and integration tests
├── Makefile            # Helper targets
├── README.md           # Project overview
└── LICENSE             # License information
```

These directories help organise code, automation and exploratory work as the
project evolves.
