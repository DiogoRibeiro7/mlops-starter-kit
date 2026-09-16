"""Service wrappers used by executable jobs."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class LoggerService:
    """Configure and expose a standard-library logger."""

    name: str = "mlops_starter_kit"
    level: int = logging.INFO
    _logger: logging.Logger = field(init=False, repr=False)

    def start(self) -> None:
        logging.basicConfig(level=self.level, force=True)
        self._logger = logging.getLogger(self.name)

    def stop(self) -> None:
        return None

    def logger(self) -> logging.Logger:
        if not hasattr(self, "_logger"):
            self.start()
        return self._logger


@dataclass
class AlertsService:
    """Notification hook with a no-op default implementation."""

    enabled: bool = False

    def start(self) -> None:
        return None

    def stop(self) -> None:
        return None

    def notify(self, message: str) -> None:
        if self.enabled:
            logging.getLogger("mlops_starter_kit").info("ALERT: %s", message)


@dataclass
class MlflowService:
    """Local tracking placeholder with an MLflow-shaped boundary."""

    tracking_dir: Path = Path("artifacts/tracking")

    def start(self) -> None:
        self.tracking_dir.mkdir(parents=True, exist_ok=True)

    def stop(self) -> None:
        return None

    def log_metric(self, run_name: str, key: str, value: float) -> None:
        path = self.tracking_dir / f"{run_name}.metrics"
        with path.open("a", encoding="utf-8") as stream:
            stream.write(f"{key}={value}\n")

    def log_params(self, run_name: str, params: dict[str, Any]) -> None:
        path = self.tracking_dir / f"{run_name}.params"
        with path.open("a", encoding="utf-8") as stream:
            for key, value in sorted(params.items()):
                stream.write(f"{key}={value}\n")
