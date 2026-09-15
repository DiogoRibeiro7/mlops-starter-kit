"""Training workflow."""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.core.models import train_baseline_classifier
from mlops_starter_kit.core.schemas import validate_training_table
from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.io.datasets import load_table, train_test_split
from mlops_starter_kit.io.provenance import (
    dataframe_fingerprint,
    write_fingerprint,
)
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.settings import ARTIFACTS_DIR

DEFAULT_TRAINING_CONFIG: dict[str, Any] = {
    "job": {"kind": "training"},
    "dataset": {
        "path": "data/raw/example.csv",
        "target_column": "target",
        "test_size": 0.2,
        "random_seed": 42,
    },
    "model": {"name": "baseline_model"},
    "artifacts": {
        "directory": str(ARTIFACTS_DIR),
        "registry": str(ARTIFACTS_DIR / "registry.json"),
    },
}


@dataclass
class TrainingJob(Job):
    """Train a baseline model and register it locally."""

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="training")
        self.config = config or DEFAULT_TRAINING_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "TrainingJob":
        return cls(load_job_config(path, DEFAULT_TRAINING_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_TRAINING_CONFIG
        dataset_config = config["dataset"]
        model_config = config["model"]
        artifact_config = config["artifacts"]

        table = load_table(dataset_config["path"])
        validate_training_table(table, dataset_config["target_column"])
        x_train, x_test, y_train, y_test = train_test_split(
            table,
            dataset_config["target_column"],
            test_size=float(dataset_config["test_size"]),
            random_state=int(dataset_config["random_seed"]),
        )

        model = train_baseline_classifier(x_train, y_train)
        metrics = classification_metrics(y_test, model.predict(x_test))

        artifact_dir = Path(artifact_config["directory"])
        artifact_dir.mkdir(parents=True, exist_ok=True)
        model_path = artifact_dir / f"{model_config['name']}.pkl"
        with model_path.open("wb") as stream:
            pickle.dump(model, stream)

        dataset_sha256 = dataframe_fingerprint(table)
        write_fingerprint(
            table, artifact_dir / "training-data.fingerprint.json"
        )
        registry = LocalModelRegistry(artifact_config["registry"])
        record = registry.register(
            model_config["name"], model_path, metrics, dataset_sha256
        )

        for key, value in metrics.items():
            self.mlflow_service.log_metric("training", key, value)

        return {
            "model": model,
            "metrics": metrics,
            "record": record,
            "model_path": model_path,
        }
