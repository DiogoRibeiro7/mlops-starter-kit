"""Classification metrics with explicit binary and multiclass behavior."""

from typing import Any, Iterable

from sklearn.metrics import accuracy_score, precision_recall_fscore_support


def classification_metrics(
    y_true: Iterable[Any], y_pred: Iterable[Any]
) -> dict[str, float]:
    """Use binary averaging for 0/1 labels, weighted averaging otherwise."""
    truth, predictions = list(y_true), list(y_pred)
    if not truth or len(truth) != len(predictions):
        raise ValueError("labels must be non-empty and have the same length")
    average = "binary" if set(truth + predictions) <= {0, 1} else "weighted"
    precision, recall, f1, _ = precision_recall_fscore_support(
        truth, predictions, average=average, zero_division=0
    )
    return {
        "accuracy": float(accuracy_score(truth, predictions)),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }
