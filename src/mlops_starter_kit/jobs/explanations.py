"""Model explanation placeholder workflow."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.settings import ARTIFACTS_DIR

DEFAULT_EXPLANATION_CONFIG: dict[str, Any] = {
    "job": {"kind": "explanations"},
    "model": {"name": "baseline_model"},
    "outputs": {"path": str(ARTIFACTS_DIR / "explanations.json")},
}


@dataclass
class ExplanationsJob(Job):
    """Write a starter explanation artifact."""

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="explanations")
        self.config = config or DEFAULT_EXPLANATION_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "ExplanationsJob":
        return cls(load_job_config(path, DEFAULT_EXPLANATION_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_EXPLANATION_CONFIG
        output_path = Path(config["outputs"]["path"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        explanation = {
            "model": config["model"]["name"],
            "method": "baseline_summary",
            "notes": (
                "Replace with SHAP, PDP or domain-specific explanation "
                "once a real model is added."
            ),
        }
        output_path.write_text(
            json.dumps(explanation, indent=2) + "\n", encoding="utf-8"
        )
        return {"explanation": explanation, "output_path": output_path}
