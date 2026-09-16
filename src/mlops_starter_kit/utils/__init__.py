"""Utility package plus backward-compatible pipeline helpers."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any, Dict, List

from pandas import DataFrame

from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.core.models import (
    create_classifier,
)
from mlops_starter_kit.io.datasets import load_table, train_test_split
from mlops_starter_kit.utils.searchers import grid_search
from mlops_starter_kit.utils.signers import model_signature
from mlops_starter_kit.utils.splitters import chronological_split


def load_data(path: Path) -> DataFrame:
    """Load a dataset from a CSV file into a :class:`DataFrame`."""
    return load_table(path)


def split_data(
    df: DataFrame,
    target_col: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[DataFrame, DataFrame, list[Any], list[Any]]:
    """Split data into train and test sets."""
    return train_test_split(df, target_col, test_size, random_state)


def train_model(
    X_train: DataFrame,
    y_train: List[Any],
    model_name: str = "baseline_model",
    **params: Any,
) -> Any:
    """Fit the requested scikit-learn estimator."""
    return create_classifier(model_name, **params).fit(X_train, y_train)


def evaluate_model(
    model: Any, X_test: DataFrame, y_test: List[Any]
) -> Dict[str, float]:
    """Compute basic classification metrics."""
    return classification_metrics(y_test, model.predict(X_test))


def save_model(model: Any, path: Path) -> None:
    """Persist the trained model to disk using :mod:`pickle`."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(model, f)


__all__ = [
    "chronological_split",
    "evaluate_model",
    "grid_search",
    "load_data",
    "model_signature",
    "save_model",
    "split_data",
    "train_model",
]
