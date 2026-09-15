"""Lightweight dataframe validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def _columns(table: Any) -> list[str]:
    return list(getattr(table, "columns", []))


@dataclass(frozen=True)
class TableSchema:
    """Expected shape for a supervised tabular dataset."""

    target_column: str = "target"
    required_columns: tuple[str, ...] = field(default_factory=tuple)

    def validate(self, table: Any) -> Any:
        """Validate that required columns exist and the table is non-empty."""
        columns = _columns(table)
        missing = [
            column
            for column in (*self.required_columns, self.target_column)
            if column not in columns
        ]
        if missing:
            raise ValueError(f"missing required columns: {', '.join(missing)}")
        if len(table) == 0:
            raise ValueError("table must contain at least one row")
        return table


def validate_training_table(table: Any, target_column: str = "target") -> Any:
    """Validate the default supervised training table."""
    return TableSchema(target_column=target_column).validate(table)
