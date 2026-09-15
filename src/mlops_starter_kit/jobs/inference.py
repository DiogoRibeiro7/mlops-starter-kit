"""Batch inference workflow."""

from __future__ import annotations

import csv
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.io.datasets import load_table
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.settings import ARTIFACTS_DIR

DEFAULT_INFERENCE_CONFIG: dict[str, Any] = {
    "job": {"kind": "inference"},
    "dataset": {"path": "data/raw/example.csv"},
    "model": {"path": str(ARTIFACTS_DIR / "baseline_model.pkl")},
    "outputs": {"path": str(ARTIFACTS_DIR / "predictions.csv")},
}


@dataclass
class InferenceJob(Job):
    """Generate predictions from a saved model."""

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="inference")
        self.config = config or DEFAULT_INFERENCE_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "InferenceJob":
        return cls(load_job_config(path, DEFAULT_INFERENCE_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_INFERENCE_CONFIG
        table = load_table(config["dataset"]["path"])
        with Path(config["model"]["path"]).open("rb") as stream:
            model = pickle.load(stream)
        predictions = model.predict(table)
        output_path = Path(config["outputs"]["path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["prediction"])
            writer.writeheader()
            writer.writerows(
                {"prediction": prediction} for prediction in predictions
            )
        return {"predictions": predictions, "output_path": output_path}
