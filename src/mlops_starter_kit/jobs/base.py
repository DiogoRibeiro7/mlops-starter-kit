"""Base classes for high-level project jobs."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any

from mlops_starter_kit.io.services import (
    AlertsService,
    LoggerService,
    MlflowService,
)

Locals = dict[str, Any]


@dataclass
class Job(abc.ABC):
    """Base context manager for executable workflows."""

    kind: str
    logger_service: LoggerService = field(default_factory=LoggerService)
    alerts_service: AlertsService = field(default_factory=AlertsService)
    mlflow_service: MlflowService = field(default_factory=MlflowService)

    def __enter__(self) -> "Job":
        self.logger_service.start()
        self.alerts_service.start()
        self.mlflow_service.start()
        self.logger_service.logger().info("Starting %s job", self.kind)
        return self

    def __exit__(
        self, exc_type: object, exc_value: object, exc_traceback: object
    ) -> bool:
        logger = self.logger_service.logger()
        if exc_value is None:
            logger.info("Finished %s job", self.kind)
        else:
            logger.exception("%s job failed", self.kind)
        self.mlflow_service.stop()
        self.alerts_service.stop()
        self.logger_service.stop()
        return False

    @abc.abstractmethod
    def run(self) -> Locals:
        """Run the job."""
