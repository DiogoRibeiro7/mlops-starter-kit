"""CSV loading and reproducible supervised dataset splits."""

import math
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split as sklearn_split

from mlops_starter_kit.core.schemas import validate_training_table


def load_table(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def split_features_target(
    table: pd.DataFrame, target_column: str
) -> tuple[pd.DataFrame, list[Any]]:
    validate_training_table(table, target_column)
    return table.drop(columns=[target_column]), table[target_column].tolist()


def train_test_split(
    table: pd.DataFrame,
    target_column: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, list[Any], list[Any]]:
    """Stratify when both partitions can represent all classes."""
    features, target = split_features_target(table, target_column)
    if len(table) < 2 or not 0 < test_size < 1:
        raise ValueError(
            "split requires at least two rows and 0 < test_size < 1"
        )
    counts = table[target_column].value_counts()
    test_rows = max(1, math.ceil(len(table) * test_size))
    stratify = (
        target
        if counts.min() >= 2
        and min(test_rows, len(table) - test_rows) >= len(counts)
        else None
    )
    x_train, x_test, y_train, y_test = sklearn_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )
    return x_train, x_test, y_train, y_test
