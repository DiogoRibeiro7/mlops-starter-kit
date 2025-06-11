"""Utility functions for the example pipeline.

These implementations avoid heavy third-party dependencies so the
unit tests can run in limited environments.
"""
from __future__ import annotations

import pickle
import random
from pathlib import Path
from typing import Iterable, Any, Dict, List

from pandas import DataFrame, read_csv


def load_data(path: Path) -> DataFrame:
    """Load a dataset from a CSV file into a :class:`DataFrame`."""
    return read_csv(path)


def split_data(
    df: DataFrame,
    target_col: str,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Split data into train and test sets."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    n = len(df)
    indices = list(range(n))
    rnd = random.Random(random_state)
    rnd.shuffle(indices)
    test_len = max(1, int(n * test_size))
    test_idx = indices[:test_len]
    train_idx = indices[test_len:]

    def subset(data: DataFrame, idxs: Iterable[int]) -> DataFrame:
        return DataFrame({col: [data[col][i] for i in idxs] for col in data.columns})

    X_train = subset(X, train_idx)
    X_test = subset(X, test_idx)
    y_train = [y[i] for i in train_idx]
    y_test = [y[i] for i in test_idx]
    return X_train, X_test, y_train, y_test


class BaselineModel:
    """Simple majority class classifier."""

    def __init__(self, majority: Any) -> None:
        self.majority = majority

    def predict(self, X: DataFrame) -> List[Any]:  # pragma: no cover - trivial
        return [self.majority for _ in range(len(X))]


def train_model(X_train: DataFrame, y_train: List[Any], model_name: str = "baseline_model", **params):
    """Train and return a very small model."""
    if model_name not in ("baseline_model", "logistic_regression", "random_forest"):
        raise ValueError(f"Unsupported model_name: {model_name}")
    majority = max(set(y_train), key=y_train.count)
    return BaselineModel(majority)


def evaluate_model(model: BaselineModel, X_test: DataFrame, y_test: List[Any]) -> Dict[str, float]:
    """Compute basic classification metrics."""
    preds = model.predict(X_test)
    tp = fp = tn = fn = 0
    for pred, true in zip(preds, y_test):
        if pred == 1 and true == 1:
            tp += 1
        elif pred == 1 and true == 0:
            fp += 1
        elif pred == 0 and true == 0:
            tn += 1
        elif pred == 0 and true == 1:
            fn += 1
    total = len(y_test)
    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0.0
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}


def save_model(model: BaselineModel, path: Path) -> None:
    """Persist the trained model to disk using :mod:`pickle`."""
    with open(path, "wb") as f:
        pickle.dump(model, f)
