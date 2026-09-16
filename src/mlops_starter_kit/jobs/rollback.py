"""Model rollback workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mlops_starter_kit.io.configs import load_job_config
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.settings import ARTIFACTS_DIR

DEFAULT_ROLLBACK_CONFIG: dict[str, Any] = {
    "job": {"kind": "rollback"},
    "registry": {"path": str(ARTIFACTS_DIR / "registry.json")},
    "rollback": {"alias": "champion", "reason": "manual rollback"},
}


@dataclass
class RollbackJob(Job):
    """Rollback a local alias to its previous target."""

    config: dict[str, Any] | None = None

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        super().__init__(kind="rollback")
        self.config = config or DEFAULT_ROLLBACK_CONFIG

    @classmethod
    def from_file(cls, path: str | Path) -> "RollbackJob":
        return cls(load_job_config(path, DEFAULT_ROLLBACK_CONFIG))

    def run(self) -> Locals:
        config = self.config or DEFAULT_ROLLBACK_CONFIG
        registry = LocalModelRegistry(config["registry"]["path"])
        target = registry.rollback(config["rollback"]["alias"])
        return {"rollback": target, "reason": config["rollback"]["reason"]}
