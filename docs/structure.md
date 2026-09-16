# Repository Structure

See [Architecture](architecture.md) for module responsibilities and
[Contributing](contributing.md) for development commands.

```text
.github/                 CI, release artifacts, issue and PR templates
.devcontainer/           Reproducible editor environment
confs/                   Validated job examples
data/                    Documented synthetic fixture
docs/                    MkDocs guides and shared-source includes
scripts/                 Cross-platform developer checks
src/mlops_starter_kit/
    core/                Estimators, metrics, feature and config contracts
    io/                  Config/data loading, artifacts, registry and tracking
    jobs/                Train, tune, evaluate, infer, explain, promote, rollback
    utils/               Shared helpers and legacy utility imports
    api.py               Prediction and health endpoints
    scripts.py           Command line interface
tests/                   Unit and end-to-end tests using real dependencies
Dockerfile               Locked builder and non-root train/serve targets
mkdocs.yml               Documentation navigation, theme and validation
pyproject.toml            Package metadata and tool configuration
poetry.lock              Resolved dependency versions
```
