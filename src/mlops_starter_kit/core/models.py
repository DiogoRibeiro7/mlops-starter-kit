"""Small reference models for the starter workflow."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence


@dataclass
class BaselineClassifier:
    """Majority-class classifier used as a portable starter model."""

    majority_class: Any | None = None

    def fit(
        self, features: object, target: Iterable[Any]
    ) -> "BaselineClassifier":
        """Fit the classifier by storing the majority target value."""
        values = list(target)
        if not values:
            raise ValueError("target must contain at least one value")
        self.majority_class = max(set(values), key=values.count)
        return self

    def predict(self, features: Sequence[Any] | object) -> list[Any]:
        """Predict the stored majority class for each input row."""
        if self.majority_class is None:
            raise ValueError("model must be fitted before prediction")
        row_count = len(features)  # type: ignore[arg-type]
        return [self.majority_class for _ in range(row_count)]


def train_baseline_classifier(
    features: object, target: Iterable[Any]
) -> BaselineClassifier:
    """Train and return the default baseline classifier."""
    return BaselineClassifier().fit(features, target)
