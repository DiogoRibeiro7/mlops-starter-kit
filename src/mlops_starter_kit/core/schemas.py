"""Tabular contracts for the numeric classification example."""

from dataclasses import dataclass

import numpy as np
import pandas as pd


def validate_features(table: pd.DataFrame) -> pd.DataFrame:
    """Require non-empty, unique, finite numeric feature columns."""
    if table.empty or not table.columns.is_unique:
        raise ValueError("features must have rows and unique columns")
    if not all(isinstance(column, str) for column in table.columns):
        raise ValueError("feature names must be strings")
    if not all(pd.api.types.is_numeric_dtype(dtype) for dtype in table.dtypes):
        raise ValueError(
            "features must be numeric; preprocess categorical columns"
        )
    if not np.isfinite(table.to_numpy(dtype=float)).all():
        raise ValueError(
            "features must not contain missing or infinite values"
        )
    return table


@dataclass(frozen=True)
class TableSchema:
    """Required columns for a labelled numeric classification table."""

    target_column: str = "target"
    required_columns: tuple[str, ...] = ()

    def validate(self, table: pd.DataFrame) -> pd.DataFrame:
        missing = set((*self.required_columns, self.target_column)) - set(
            table.columns
        )
        if missing:
            raise ValueError(
                f"missing required columns: {', '.join(sorted(missing))}"
            )
        if not table.columns.is_unique:
            raise ValueError("table columns must be unique")
        validate_features(table.drop(columns=[self.target_column]))
        if table[self.target_column].isna().any():
            raise ValueError("target must not contain missing values")
        return table


def validate_training_table(
    table: pd.DataFrame, target_column: str = "target"
) -> pd.DataFrame:
    """Validate feature and target columns before training or evaluation."""
    return TableSchema(target_column=target_column).validate(table)
