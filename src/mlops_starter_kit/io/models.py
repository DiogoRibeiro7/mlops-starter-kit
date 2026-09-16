"""Resolve model references consistently across inference consumers."""

from pathlib import Path

from mlops_starter_kit.core.configs import ModelReference
from mlops_starter_kit.core.models import ModelArtifact
from mlops_starter_kit.io.artifacts import load_artifact
from mlops_starter_kit.io.registries import LocalModelRegistry


def resolve_model(reference: ModelReference) -> ModelArtifact:
    if reference.path is not None:
        return load_artifact(reference.path)
    record = LocalModelRegistry(reference.registry).get(
        reference.name, reference.version, reference.alias
    )
    return load_artifact(Path(record.path), record.artifact_sha256)
