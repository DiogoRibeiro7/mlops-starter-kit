"""Registry integrity, concurrency, quality gates and rollback history."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

import pytest

from mlops_starter_kit.io.registries import LocalModelRegistry


@pytest.fixture
def registry(tmp_path):
    return LocalModelRegistry(tmp_path / "registry.json")


@pytest.fixture
def artifact(tmp_path):
    path = tmp_path / "source.pkl"
    path.write_bytes(b"original model")
    return path


def test_register_snapshots_source_and_preserves_old_versions(
    registry, artifact
):
    first = registry.register("model", artifact, {"accuracy": 0.8}, "data")
    artifact.write_bytes(b"retrained model")
    second = registry.register("model", artifact, {"accuracy": 0.9}, "data")
    assert Path(first.path).read_bytes() == b"original model"
    assert Path(second.path).read_bytes() == b"retrained model"
    assert first.artifact_sha256 != second.artifact_sha256
    assert registry.get("model").version == 2
    assert registry.get("model", 1) == first


def test_concurrent_registration_never_loses_versions(registry, artifact):
    def register(_):
        return registry.register("model", artifact, {"accuracy": 0.8}, "data")

    with ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(register, range(12)))
    assert sorted(record.version for record in records) == list(range(1, 13))
    assert len({record.path for record in records}) == 12
    assert registry.get("model").version == 12


def test_promotion_requires_existing_intact_qualified_model(
    registry, artifact
):
    registry.register("model", artifact, {"accuracy": 0.6}, "data")
    with pytest.raises(ValueError, match="not registered"):
        registry.promote("model", 7)
    with pytest.raises(ValueError, match="threshold"):
        registry.promote("model", 1, min_accuracy=0.8)
    registry.promote("model", 1, min_accuracy=0.5)
    assert registry.get(alias="champion").version == 1
    Path(registry.get("model").path).write_bytes(b"corrupted")
    with pytest.raises(ValueError, match="checksum"):
        registry.promote("model", 1)


def test_repeated_rollback_walks_back_multiple_promotions(registry, artifact):
    for _ in range(3):
        record = registry.register(
            "model", artifact, {"accuracy": 0.9}, "data"
        )
        registry.promote("model", record.version)
    registry.promote("model", 3)
    assert registry.rollback(reason="regression")["version"] == 2
    assert registry.rollback()["version"] == 1
    with pytest.raises(ValueError, match="no previous"):
        registry.rollback()
    assert registry.get(alias="champion").version == 1
    state = json.loads(registry.path.read_text())
    assert state["history"][-2]["reason"] == "regression"


def test_missing_alias_is_explicit(registry):
    with pytest.raises(ValueError, match="has no model"):
        registry.get(alias="unknown")


@pytest.mark.parametrize("name", ["../escape", "/absolute", "", "a/b"])
def test_invalid_names_cannot_escape_registry(registry, artifact, name):
    with pytest.raises(ValueError):
        registry.register(name, artifact, {"accuracy": 1.0}, "data")


def test_invalid_metrics_and_missing_file_are_rejected(registry, artifact):
    with pytest.raises(ValueError, match="finite"):
        registry.register(
            "model", artifact, {"accuracy": float("nan")}, "data"
        )
    with pytest.raises(FileNotFoundError):
        registry.register(
            "model", artifact.parent / "missing", {"accuracy": 1}, "data"
        )


def test_failed_metadata_write_does_not_publish_version(
    registry, artifact, monkeypatch
):
    from mlops_starter_kit.io import registries

    original = registries.write_json

    def fail_write(*args):
        raise OSError("disk failure")

    monkeypatch.setattr(registries, "write_json", fail_write)
    with pytest.raises(OSError, match="disk failure"):
        registry.register("model", artifact, {"accuracy": 1}, "data")
    assert not registry.path.exists()
    monkeypatch.setattr(registries, "write_json", original)
    assert (
        registry.register("model", artifact, {"accuracy": 1}, "data").version
        == 1
    )


def test_partial_snapshot_is_cleaned_up(registry, artifact, monkeypatch):
    import shutil

    original = shutil.copyfileobj

    def interrupted_copy(incoming, output):
        output.write(b"partial")
        raise OSError("interrupted write")

    monkeypatch.setattr(shutil, "copyfileobj", interrupted_copy)
    with pytest.raises(OSError, match="interrupted write"):
        registry.register("model", artifact, {"accuracy": 1}, "data")
    assert not list(registry.path.parent.rglob("v*.pkl"))
    monkeypatch.setattr(shutil, "copyfileobj", original)
    assert (
        registry.register("model", artifact, {"accuracy": 1}, "data").version
        == 1
    )
