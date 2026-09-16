"""Local model registry primitives."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ModelRecord:
    """Metadata for a locally persisted model."""

    name: str
    version: int
    path: str
    metrics: dict[str, float]
    dataset_sha256: str


class LocalModelRegistry:
    """Small JSON-backed registry used by the starter workflows."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"models": {}, "aliases": {}, "history": []}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, state: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(state, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def register(
        self,
        name: str,
        path: str | Path,
        metrics: dict[str, float],
        dataset_sha256: str,
    ) -> ModelRecord:
        """Register a model artifact and return its record."""
        state = self._read()
        records = state["models"].setdefault(name, [])
        version = len(records) + 1
        record = ModelRecord(
            name=name,
            version=version,
            path=str(path),
            metrics=metrics,
            dataset_sha256=dataset_sha256,
        )
        records.append(asdict(record))
        self._write(state)
        return record

    def promote(
        self, name: str, version: int, alias: str = "champion"
    ) -> dict[str, Any]:
        """Point an alias at a registered model version."""
        state = self._read()
        previous = state["aliases"].get(alias)
        candidate = {"name": name, "version": version}
        state["aliases"][alias] = candidate
        state["history"].append(
            {
                "action": "promote",
                "alias": alias,
                "previous": previous,
                "target": candidate,
            }
        )
        self._write(state)
        return {"previous": previous, "target": candidate}

    def rollback(self, alias: str = "champion") -> dict[str, Any]:
        """Restore an alias to the previous promotion target."""
        state = self._read()
        promotions = [
            item
            for item in state.get("history", [])
            if item.get("action") == "promote" and item.get("alias") == alias
        ]
        if not promotions or not promotions[-1].get("previous"):
            raise ValueError(f"alias {alias!r} has no previous target")
        target = promotions[-1]["previous"]
        state["aliases"][alias] = target
        state["history"].append(
            {"action": "rollback", "alias": alias, "target": target}
        )
        self._write(state)
        return target
