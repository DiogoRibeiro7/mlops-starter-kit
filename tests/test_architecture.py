from __future__ import annotations

import json
from pathlib import Path

from pandas import DataFrame

from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.core.schemas import validate_training_table
from mlops_starter_kit.io.configs import load_config_file, merge_dicts
from mlops_starter_kit.io.provenance import dataframe_fingerprint
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.jobs.training import TrainingJob
from mlops_starter_kit.scripts import job_from_config, schema
from mlops_starter_kit.utils import (
    chronological_split,
    grid_search,
    model_signature,
)


def test_config_loader_reads_nested_yaml(tmp_path: Path) -> None:
    path = tmp_path / "training.yaml"
    path.write_text(
        "job:\n"
        "  kind: training\n"
        "dataset:\n"
        "  path: data/raw/example.csv\n"
        "  test_size: 0.2\n",
        encoding="utf-8",
    )

    config = load_config_file(path)

    assert config["job"]["kind"] == "training"
    assert config["dataset"]["test_size"] == 0.2


def test_merge_dicts_merges_nested_values() -> None:
    merged = merge_dicts({"a": {"b": 1, "c": 2}}, {"a": {"b": 3}})
    assert merged == {"a": {"b": 3, "c": 2}}


def test_core_metrics_and_schema() -> None:
    table = DataFrame({"feature": [1, 2, 3], "target": [0, 1, 1]})
    assert validate_training_table(table, "target") is table

    metrics = classification_metrics([0, 1, 1], [0, 1, 0])

    assert metrics["accuracy"] == 2 / 3
    assert set(metrics) == {"accuracy", "precision", "recall", "f1"}


def test_provenance_is_stable() -> None:
    table = DataFrame({"feature": [1, 2], "target": [0, 1]})

    assert dataframe_fingerprint(table) == dataframe_fingerprint(table)


def test_registry_promote_and_rollback(tmp_path: Path) -> None:
    registry = LocalModelRegistry(tmp_path / "registry.json")
    (tmp_path / "first.pkl").write_bytes(b"first model")
    (tmp_path / "second.pkl").write_bytes(b"second model")
    first = registry.register(
        "baseline", tmp_path / "first.pkl", {"accuracy": 0.5}, "aaa"
    )
    second = registry.register(
        "baseline", tmp_path / "second.pkl", {"accuracy": 0.7}, "bbb"
    )

    registry.promote(first.name, first.version)
    registry.promote(second.name, second.version)
    target = registry.rollback()

    assert target == {"name": "baseline", "version": 1}


def test_utility_helpers() -> None:
    assert chronological_split([1, 2, 3, 4], 2) == ([1, 2], [3, 4])
    assert grid_search([{"x": 1}, {"x": 2}], lambda item: item["x"])["x"] == 2
    assert model_signature(DataFrame({"a": [1], "b": [2]})) == {
        "inputs": ["a", "b"],
        "rows": 1,
    }


def test_training_job_registers_model(tmp_path: Path) -> None:
    data_path = tmp_path / "data.csv"
    data_path.write_text(
        "feature,target\n1,0\n2,1\n3,1\n4,1\n", encoding="utf-8"
    )
    artifact_dir = tmp_path / "artifacts"
    config = {
        "job": {"kind": "training"},
        "dataset": {
            "path": str(data_path),
            "target_column": "target",
            "test_size": 0.25,
            "random_seed": 0,
        },
        "model": {"name": "baseline_model"},
        "artifacts": {
            "directory": str(artifact_dir),
            "registry": str(artifact_dir / "registry.json"),
        },
    }

    with TrainingJob(config) as job:
        result = job.run()

    registry = json.loads(
        (artifact_dir / "registry.json").read_text(encoding="utf-8")
    )
    assert result["model_path"].exists()
    assert registry["models"]["baseline_model"][0]["version"] == 1


def test_cli_schema_and_job_factory(tmp_path: Path) -> None:
    config_path = tmp_path / "tuning.yaml"
    config_path.write_text(
        "job:\n  kind: tuning\nsearch:\n  parameters:\n    C: [0.1, 1]\n",
        encoding="utf-8",
    )

    assert "training" in schema()["job_kinds"]
    assert job_from_config(config_path).kind == "tuning"
