"""Model promotion workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.settings import ARTIFACTS_DIR

DEFAULT_PROMOTION_CONFIG: dict[str, Any] = {
    "job": {"kind": "promotion"},
    "registry": {"path": str(ARTIFACTS_DIR / "registry.json")},
    "model": {"name": "baseline_model", "version": 1},
    "promotion": {"alias": "champion"},
}


@dataclass
class PromotionJob(Job):
    """Promote a registered model version to a local alias."""

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="promotion")
        self.config = config or DEFAULT_PROMOTION_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "PromotionJob":
        return cls(load_job_config(path, DEFAULT_PROMOTION_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_PROMOTION_CONFIG
        registry = LocalModelRegistry(config["registry"]["path"])
        result = registry.promote(
            config["model"]["name"],
            int(config["model"]["version"]),
            config["promotion"]["alias"],
        )
        return {"promotion": result}
