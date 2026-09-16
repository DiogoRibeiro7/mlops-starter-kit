"""Dataset and artifact fingerprint helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def _value_at(column: Any, index: int) -> Any:
    if hasattr(column, "iloc"):
        return column.iloc[index]
    return column[index]


def dataframe_fingerprint(table: Any) -> str:
    """Return a stable SHA-256 fingerprint for a dataframe-like object."""
    columns = list(getattr(table, "columns", []))
    payload = {
        "columns": columns,
        "rows": [
            {column: _value_at(table[column], index) for column in columns}
            for index in range(len(table))
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def write_fingerprint(table: Any, path: str | Path) -> str:
    """Write table fingerprint metadata and return the digest."""
    digest = dataframe_fingerprint(table)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"sha256": digest}, indent=2) + "\n", encoding="utf-8"
    )
    return digest
