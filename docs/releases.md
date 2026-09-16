# Releases

The package is pre-1.0. Public interfaces may change; migration notes belong in
[the changelog](changelog.md). Use semantic version tags of the form
`vMAJOR.MINOR.PATCH`.

1. Update `project.version` in `pyproject.toml` and add a dated changelog section.
2. Run `poetry check --lock`, the full check command and `poetry build`.
3. Merge the release PR after all CI jobs pass.
4. Create the matching version tag. The release workflow verifies the tag,
   checks/tests the package, builds the wheel and source archive and uploads them.
5. Review the artifacts and publish through the organization's release process.

Python distributions are not automatically published to PyPI. Configure a
trusted publisher and an approval-protected release environment before adding
that step. Docker publication uses the existing `DOCKERHUB_USERNAME` and
`DOCKERHUB_TOKEN` secrets; configure them before tagging or manually running
the Docker Build workflow.

Branch protection, required CI checks and private vulnerability reporting are
repository settings. Maintainers should enable them in GitHub; changing files
in this repository does not enable those settings.
