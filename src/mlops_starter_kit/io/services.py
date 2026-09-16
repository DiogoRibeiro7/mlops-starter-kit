"""Local run tracking with unique records for successful and failed jobs."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from mlops_starter_kit.io.artifacts import write_json


class LocalTrackingService:
    """Keep each run's configuration, metrics and outcome in one JSON file."""

    def __init__(
        self, directory: Path, kind: str, config: dict[str, Any]
    ) -> None:
        self.run_id = uuid4().hex
        self.path = directory / f"{self.run_id}.json"
        self.record: dict[str, Any] = {
            "run_id": self.run_id,
            "kind": kind,
            "config": config,
            "metrics": {},
            "status": "created",
        }

    def start(self) -> None:
        self.record.update(
            status="running", started_at=datetime.now(timezone.utc).isoformat()
        )
        write_json(self.path, self.record)

    def log_metrics(self, metrics: dict[str, float]) -> None:
        self.record["metrics"].update(metrics)
        write_json(self.path, self.record)

    def finish(self, error: BaseException | None = None) -> None:
        self.record.update(
            status="failed" if error else "completed",
            finished_at=datetime.now(timezone.utc).isoformat(),
        )
        if error:
            self.record["error"] = str(error)
        write_json(self.path, self.record)
