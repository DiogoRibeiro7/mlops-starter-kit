"""Evaluation workflow."""

from __future__ import annotations

import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.core.schemas import validate_training_table
from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.io.datasets import load_table, split_features_target
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.settings import ARTIFACTS_DIR

DEFAULT_EVALUATION_CONFIG: dict[str, Any] = {
    "job": {"kind": "evaluations"},
    "dataset": {"path": "data/raw/example.csv", "target_column": "target"},
    "model": {"path": str(ARTIFACTS_DIR / "baseline_model.pkl")},
}


@dataclass
class EvaluationsJob(Job):
    """Evaluate a saved model artifact against a labelled dataset."""

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="evaluations")
        self.config = config or DEFAULT_EVALUATION_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "EvaluationsJob":
        return cls(load_job_config(path, DEFAULT_EVALUATION_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_EVALUATION_CONFIG
        table = load_table(config["dataset"]["path"])
        validate_training_table(table, config["dataset"]["target_column"])
        features, target = split_features_target(
            table, config["dataset"]["target_column"]
        )
        with Path(config["model"]["path"]).open("rb") as stream:
            model = pickle.load(stream)
        metrics = classification_metrics(target, model.predict(features))
        for key, value in metrics.items():
            self.mlflow_service.log_metric("evaluations", key, value)
        return {"metrics": metrics}
