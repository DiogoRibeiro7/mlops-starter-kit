"""Metric functions used by jobs and tests."""

from __future__ import annotations

from typing import Any, Iterable


def classification_metrics(
    y_true: Iterable[Any], y_pred: Iterable[Any]
) -> dict[str, float]:
    """Return accuracy, precision, recall and F1 for binary labels.

    The starter kit intentionally keeps this implementation dependency-light.
    For multiclass work, replace this function with scikit-learn metrics.
    """
    true_values = list(y_true)
    pred_values = list(y_pred)
    if len(true_values) != len(pred_values):
        raise ValueError("y_true and y_pred must have the same length")

    tp = fp = tn = fn = 0
    for truth, prediction in zip(true_values, pred_values):
        if prediction == 1 and truth == 1:
            tp += 1
        elif prediction == 1 and truth == 0:
            fp += 1
        elif prediction == 0 and truth == 0:
            tn += 1
        elif prediction == 0 and truth == 1:
            fn += 1

    total = len(true_values)
    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall)
        else 0.0
    )
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }
