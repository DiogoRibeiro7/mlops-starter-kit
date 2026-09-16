"""A local registry with immutable snapshots and serialized transactions."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import shutil
from typing import Any

from filelock import FileLock
from pydantic import TypeAdapter

from mlops_starter_kit.core.configs import Name
from mlops_starter_kit.io.artifacts import file_sha256, write_json

_NAME = TypeAdapter(Name)


@dataclass(frozen=True)
class ModelRecord:
    name: str
    version: int
    path: str
    metrics: dict[str, float]
    dataset_sha256: str
    artifact_sha256: str
    created_at: str


class LocalModelRegistry:
    """Coordinate local writers using a file lock and atomic JSON updates."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = FileLock(str(self.path) + ".lock", timeout=30)

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"models": {}, "aliases": {}, "history": [], "stacks": {}}
        state = json.loads(self.path.read_text(encoding="utf-8"))
        state.setdefault("stacks", {})
        return state

    def _record(
        self, state: dict[str, Any], name: str, version: int | None
    ) -> ModelRecord:
        records = state["models"].get(name, [])
        selected = [
            row
            for row in records
            if version is None or row["version"] == version
        ]
        if not selected:
            raise ValueError(
                f"model {name!r} version {version!r} is not registered"
            )
        return ModelRecord(**selected[-1])

    def _verify(self, record: ModelRecord) -> None:
        if file_sha256(Path(record.path)) != record.artifact_sha256:
            raise ValueError(
                "model artifact checksum does not match the registry"
            )

    def register(
        self,
        name: str,
        path: str | Path,
        metrics: dict[str, float],
        dataset_sha256: str,
    ) -> ModelRecord:
        """Snapshot an artifact before publishing its immutable version."""
        _NAME.validate_python(name)
        source = Path(path).resolve(strict=True)
        if not metrics or not all(
            math.isfinite(value) for value in metrics.values()
        ):
            raise ValueError("model metrics must be non-empty and finite")
        with self.lock:
            state = self._read()
            records = state["models"].setdefault(name, [])
            version = max((row["version"] for row in records), default=0) + 1
            destination = (
                self.path.parent / "models" / name / f"v{version}.pkl"
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            created = False
            try:
                # Publish metadata only after the complete snapshot is on disk.
                with destination.open("xb") as output:
                    created = True
                    with source.open("rb") as incoming:
                        shutil.copyfileobj(incoming, output)
                record = ModelRecord(
                    name,
                    version,
                    str(destination),
                    dict(metrics),
                    dataset_sha256,
                    file_sha256(destination),
                    datetime.now(timezone.utc).isoformat(),
                )
                records.append(asdict(record))
                write_json(self.path, state)
            except Exception:
                if created:
                    destination.unlink(missing_ok=True)
                raise
            return record

    def get(
        self,
        name: str = "baseline_model",
        version: int | None = None,
        alias: str | None = None,
    ) -> ModelRecord:
        """Resolve a version or alias and verify its artifact is unchanged."""
        with self.lock:
            state = self._read()
            if alias is not None:
                target = state["aliases"].get(alias)
                if target is None:
                    raise ValueError(f"alias {alias!r} has no model")
                name, version = target["name"], target["version"]
            record = self._record(state, name, version)
            self._verify(record)
            return record

    def promote(
        self,
        name: str,
        version: int,
        alias: str = "champion",
        min_accuracy: float = 0.0,
    ) -> dict[str, Any]:
        """Promote an existing intact version that meets its accuracy gate."""
        _NAME.validate_python(alias)
        if not 0 <= min_accuracy <= 1:
            raise ValueError("minimum accuracy must be between 0 and 1")
        with self.lock:
            state = self._read()
            record = self._record(state, name, version)
            self._verify(record)
            if record.metrics.get("accuracy", -1) < min_accuracy:
                raise ValueError(
                    "model does not meet the promotion accuracy threshold"
                )
            previous = state["aliases"].get(alias)
            target = {"name": name, "version": version}
            if previous != target:
                state["stacks"].setdefault(alias, []).append(previous)
                state["aliases"][alias] = target
                state["history"].append(
                    {
                        "action": "promote",
                        "alias": alias,
                        "previous": previous,
                        "target": target,
                        "at": datetime.now(timezone.utc).isoformat(),
                    }
                )
                write_json(self.path, state)
            return {"previous": previous, "target": target}

    def rollback(
        self, alias: str = "champion", reason: str = "manual rollback"
    ) -> dict[str, Any]:
        """Restore earlier promotions in order."""
        with self.lock:
            state = self._read()
            stack = state["stacks"].get(alias, [])
            if not stack or stack[-1] is None:
                raise ValueError(f"alias {alias!r} has no previous target")
            target = stack.pop()
            self._verify(
                self._record(state, target["name"], target["version"])
            )
            state["aliases"][alias] = target
            state["history"].append(
                {
                    "action": "rollback",
                    "alias": alias,
                    "target": target,
                    "reason": reason,
                    "at": datetime.now(timezone.utc).isoformat(),
                }
            )
            write_json(self.path, state)
            return target
