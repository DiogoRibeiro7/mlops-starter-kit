# Documentation

The site uses [MkDocs](https://www.mkdocs.org/) with
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).
Its optional Poetry group keeps documentation tooling out of the runtime
package and Docker images; `poetry.lock` pins the build environment.

## Local Preview

From the repository root:

```bash
poetry sync --with docs
poetry run mkdocs serve
```

Open `http://127.0.0.1:8001/mlops-starter-kit/`. The separate port leaves
8000 available for the prediction API. When 8001 is occupied, use
`poetry run mkdocs serve --dev-addr 127.0.0.1:8002`.

## Build and Validate

```bash
poetry check --lock
poetry run mkdocs build --strict
```

The generated site is written to the ignored `site/` directory. Missing pages,
broken internal links or anchors, unlisted navigation pages and build warnings
fail the strict build. External HTTP links are not checked by MkDocs.
`make docs` and `just docs` run the same build; their `docs-serve` commands
start the preview server.

For a documentation-only environment, use
`poetry sync --only docs --no-root`. This removes application and development
dependencies from that environment; restore them with `poetry sync --with docs`
before running application checks.

## Edit Content

Edit guides under `docs/` and register new pages in the `nav` section of
`mkdocs.yml`. Use relative Markdown links so the strict build can validate
and rewrite them for the deployed site. Mermaid code fences render the
architecture diagram; code tabs support Bash and PowerShell examples.

Contribution, security, changelog and dataset pages include their canonical
files (`CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md` and `data/README.md`).
Edit those source files, not copied content. The include plugin rewrites their
relative links, and the preview server watches them for changes. Includes are
local-only, so site builds do not fetch remote Markdown.

## GitHub Pages

The `Documentation` workflow builds every pull request to `main`. PRs cannot
deploy and have read-only repository permissions. Pushes to `main`, or a manual
workflow run on `main`, build and publish the tested site artifact to GitHub
Pages. Only the deploy job receives `pages: write` and `id-token: write`.

For a new fork, enable **Settings > Pages > Build and deployment > Source >
GitHub Actions** and restrict the `github-pages` environment to `main`.
Update `site_url`, `repo_url`, `repo_name` and the package documentation URL
for the new repository. No personal access token or `gh-pages` branch is needed.

The configured publication address is
<https://diogoribeiro7.github.io/mlops-starter-kit/>. It becomes available after
the first successful deployment. The site follows `main`; versioned release
documentation is not configured.

If a deployment fails, check Pages settings, environment branch restrictions
and the workflow's permissions. Re-run the workflow on `main` after correcting
the configuration. Do not bypass a failed strict build to publish.
