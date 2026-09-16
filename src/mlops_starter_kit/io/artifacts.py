"""Atomic metadata writes and persistence of trusted local model artifacts."""

from dataclasses import asdict, is_dataclass
import hashlib
import json
import os
from pathlib import Path
import pickle
import tempfile
from typing import Any

import numpy as np

from mlops_starter_kit.core.models import ModelArtifact


def json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot encode {type(value).__name__} as JSON")


def write_json(path: Path, data: Any) -> None:
    """Replace a complete JSON document atomically on the same filesystem."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(
                data, stream, indent=2, allow_nan=False, default=json_default
            )
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def save_artifact(artifact: ModelArtifact, path: Path) -> None:
    """Create an artifact without overwriting an existing model."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        pickle.dump(artifact, stream, protocol=pickle.HIGHEST_PROTOCOL)


def load_artifact(
    path: Path, expected_sha256: str | None = None
) -> ModelArtifact:
    """Load a trusted artifact, checking its registered digest when supplied.

    Pickle can execute code. Only load artifacts produced in a trusted
    environment; a checksum detects corruption, not a malicious publisher.
    """
    payload = path.read_bytes()
    if (
        expected_sha256
        and hashlib.sha256(payload).hexdigest() != expected_sha256
    ):
        raise ValueError("model artifact checksum does not match the registry")
    artifact = pickle.loads(payload)
    if not isinstance(artifact, ModelArtifact):
        raise ValueError(
            "unsupported artifact format; retrain with this version"
        )
    return artifact
