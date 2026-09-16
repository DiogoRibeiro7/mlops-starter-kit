"""Hyperparameter tuning placeholder workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.jobs.base import Job, Locals

DEFAULT_TUNING_CONFIG: dict[str, Any] = {
    "job": {"kind": "tuning"},
    "search": {"model_names": "baseline_model"},
}


@dataclass
class TuningJob(Job):
    """Select starter hyperparameters.

    This is intentionally simple; replace it with Optuna, Ray Tune or
    scikit-learn search once the project owns real model candidates.
    """

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="tuning")
        self.config = config or DEFAULT_TUNING_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "TuningJob":
        return cls(load_job_config(path, DEFAULT_TUNING_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_TUNING_CONFIG
        return {"best_params": {"model_name": config["search"]["model_names"]}}
