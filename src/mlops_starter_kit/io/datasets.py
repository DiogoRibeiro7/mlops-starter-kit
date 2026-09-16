"""Dataset loading and splitting helpers."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Any, Iterable

from pandas import DataFrame, read_csv


def _value_at(column: Any, index: int) -> Any:
    if hasattr(column, "iloc"):
        return column.iloc[index]
    return column[index]


def _subset(table: DataFrame, indices: Iterable[int]) -> DataFrame:
    index_list = list(indices)
    return DataFrame(
        {
            column: [_value_at(table[column], index) for index in index_list]
            for column in list(table.columns)
        }
    )


def load_table(path: str | Path) -> DataFrame:
    """Load a CSV table."""
    return read_csv(path)


def split_features_target(
    table: DataFrame, target_column: str
) -> tuple[DataFrame, list[Any]]:
    """Split a supervised table into features and target values."""
    features = table.drop(columns=[target_column])
    target = [
        _value_at(table[target_column], index) for index in range(len(table))
    ]
    return features, target


def train_test_split(
    table: DataFrame,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[DataFrame, DataFrame, list[Any], list[Any]]:
    """Split rows into train/test partitions."""
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")
    indices = list(range(len(table)))
    random.Random(random_state).shuffle(indices)
    test_len = max(1, int(len(indices) * test_size))
    test_indices = indices[:test_len]
    train_indices = indices[test_len:]

    train_table = _subset(table, train_indices)
    test_table = _subset(table, test_indices)
    x_train, y_train = split_features_target(train_table, target_column)
    x_test, y_test = split_features_target(test_table, target_column)
    return x_train, x_test, y_train, y_test
