# Contributing

## Environment

Use Python 3.10-3.14 and Poetry 2.2.1. Python 3.13 is the default development
version. Run `poetry sync` to install exactly the locked dependencies and
`poetry run pre-commit install` to enable the local hooks. VS Code can open
the supplied `.devcontainer/` environment.

## Changes

Create a short-lived branch from `main`. Keep changes focused and include
regression tests for changes to configuration, artifacts or public behavior.
Tests use actual pandas, scikit-learn and FastAPI installations. Do not add
modules that shadow third-party packages or alter `sys.path` in tests.

Before opening a pull request:

```bash
poetry check --lock
poetry run python scripts/check.py
poetry build
```

Use `poetry run black src tests scripts` to apply formatting. A PR should
describe the problem, resulting behavior and validation. Update the docs
and `CHANGELOG.md` when changing a public workflow. Maintainers should merge
only after all CI jobs pass.

## Roadmap Work

Use the [next-work queue](docs/roadmap.md#next-work-queue) to select planned work.
Before implementing a roadmap task, open an issue with its stable task ID,
proposed owner, scope, dependencies and acceptance tests. Agree scope with a
maintainer, link the issue from the PR and include validation evidence.
Bug fixes and small maintenance changes do not need a roadmap milestone.

Update the [delivery plan](docs/roadmap.md#tracking-and-review) in the same PR
when progress changes. Keep tasks incomplete until their acceptance criteria
are met; distinguish implemented code from released or operationally verified
capabilities. Propose scope or priority changes explicitly instead of silently
adding a new integration to an existing task.

## Dependencies

Declare directly imported dependencies in `pyproject.toml`; keep optional
integrations in extras. Run `poetry lock` after changes and commit the lockfile.
Pre-commit, local checks and CI use the same Poetry environment and tool
configuration. Recheck the oldest supported Python after dependency updates.

## Documentation

```bash
poetry sync --with docs
poetry run mkdocs serve
poetry run mkdocs build --strict
```

The preview uses port 8001. Documentation changes must pass the strict build,
including internal links and anchors. See the
[documentation guide](docs/documentation.md) for navigation, shared source files
and GitHub Pages deployment. The docs dependency group is optional and is not
installed by the normal `poetry sync` command.

## Data and Artifacts

Use temporary directories in tests. Never commit real credentials, private
datasets, trained model files or generated run records. The synthetic example
data and its provenance are documented in `data/README.md`.

## Reporting Problems

Include the Python version, operating system, command, sanitized configuration
and relevant error output. Report vulnerabilities using the
[security policy](https://github.com/DiogoRibeiro7/mlops-starter-kit/blob/main/SECURITY.md),
not a public issue containing exploit details or credentials.
