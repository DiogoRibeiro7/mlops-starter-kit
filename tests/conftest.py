"""Isolated filesystem fixtures shared by unit and integration tests."""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(autouse=True)
def isolated_working_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MODEL_PATH", raising=False)


@pytest.fixture
def dataset(tmp_path: Path) -> Path:
    path = tmp_path / "dataset.csv"
    pd.DataFrame(
        {
            "feature1": list(range(24)),
            "feature2": [value / 2 for value in range(24)],
            "target": [0] * 12 + [1] * 12,
        }
    ).to_csv(path, index=False)
    return path


@pytest.fixture
def training_config(tmp_path, dataset):
    return {
        "job": {"kind": "training"},
        "dataset": {"path": str(dataset)},
        "model": {"name": "example", "algorithm": "logistic_regression"},
        "artifacts": {
            "directory": str(tmp_path / "artifacts"),
            "registry": str(tmp_path / "registry.json"),
        },
        "tracking": {"directory": str(tmp_path / "tracking")},
    }
