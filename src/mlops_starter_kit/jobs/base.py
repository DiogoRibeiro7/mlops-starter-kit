"""Shared configuration, logging and tracking lifecycle for jobs."""

from abc import ABC, abstractmethod
import logging
from pathlib import Path
from types import TracebackType
from typing import Any, ClassVar, Generic, TypeVar

from mlops_starter_kit.core.configs import JobConfig
from mlops_starter_kit.io.configs import load_config_file
from mlops_starter_kit.io.services import LocalTrackingService

ConfigT = TypeVar("ConfigT", bound=JobConfig)
Locals = dict[str, Any]


class Job(ABC, Generic[ConfigT]):
    """Validate before execution and retain a distinct record for every run."""

    kind: ClassVar[str]
    config_type: type[ConfigT]

    def __init__(self, config: dict[str, Any] | ConfigT | None = None) -> None:
        self.config = self.config_type.model_validate(config or {})
        if self.config.job.kind != self.kind:
            raise ValueError(f"expected job kind {self.kind!r}")
        self.tracking = LocalTrackingService(
            self.config.tracking.directory,
            self.kind,
            self.config.model_dump(mode="json"),
        )
        self.logger = logging.getLogger(f"mlops_starter_kit.jobs.{self.kind}")

    @classmethod
    def from_file(cls, path: str | Path) -> "Job[ConfigT]":
        return cls(load_config_file(path))

    def __enter__(self) -> "Job[ConfigT]":
        self.tracking.start()
        self.logger.info("Starting %s run %s", self.kind, self.tracking.run_id)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.tracking.finish(exc_value)
        self.logger.info("Finished %s run %s", self.kind, self.tracking.run_id)

    @abstractmethod
    def run(self) -> Locals:
        """Execute a validated workflow."""
