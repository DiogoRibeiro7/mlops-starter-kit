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
├── Makefile            # Placeholder helper targets
├── README.md           # Project overview
└── LICENSE             # License information
```

Directories such as `src/`, `data/`, `tests/` and CI/CD workflows can be added
later as the project evolves.
