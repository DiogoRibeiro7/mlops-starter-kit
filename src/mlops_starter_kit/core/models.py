"""Deterministic scikit-learn estimators and their persisted input schema."""

from dataclasses import dataclass
from typing import Any, Iterable

import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from mlops_starter_kit.core.schemas import validate_features


class BaselineClassifier(DummyClassifier):
    """Majority-class benchmark with the standard estimator interface."""

    def __init__(self, random_state: int = 42) -> None:
        super().__init__(strategy="most_frequent", random_state=random_state)


def create_classifier(
    algorithm: str = "baseline_model",
    random_seed: int = 42,
    **parameters: Any,
) -> Any:
    """Construct an estimator, rejecting unsupported names and parameters."""
    constructors = {
        "baseline_model": BaselineClassifier,
        "logistic_regression": LogisticRegression,
        "random_forest": RandomForestClassifier,
    }
    if algorithm not in constructors:
        raise ValueError(f"Unsupported model_name: {algorithm}")
    options = {"random_state": random_seed, **parameters}
    if algorithm == "logistic_regression":
        options.setdefault("max_iter", 1000)
    return constructors[algorithm](**options)


def train_baseline_classifier(
    features: pd.DataFrame, target: Iterable[Any]
) -> BaselineClassifier:
    """Fit a majority-class benchmark."""
    return BaselineClassifier().fit(features, list(target))


@dataclass
class ModelArtifact:
    """Bundle a fitted estimator with its feature order and target name."""

    estimator: Any
    features: tuple[str, ...]
    target_column: str
    algorithm: str

    def prepare(self, table: pd.DataFrame) -> pd.DataFrame:
        """Validate and order features consistently for every prediction."""
        features = table.drop(columns=[self.target_column], errors="ignore")
        if set(features.columns) != set(self.features):
            raise ValueError(
                f"expected feature columns: {', '.join(self.features)}"
            )
        return validate_features(features.loc[:, list(self.features)])

    def predict(self, table: pd.DataFrame) -> list[Any]:
        """Return native Python predictions suitable for JSON responses."""
        return self.estimator.predict(self.prepare(table)).tolist()
