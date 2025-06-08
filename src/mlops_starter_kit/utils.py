# src/mlops_starter_kit/utils.py

from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
import joblib


def load_data(path: Path) -> pd.DataFrame:
    """
    Load a dataset from a CSV file.
    """
    df = pd.read_csv(path)
    return df


def split_data(
    df: pd.DataFrame,
    target_col: str,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Split DataFrame into train and test sets.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def train_model(X_train, y_train, model_name: str = "baseline_model", **params):
    """
    Train and return a scikit-learn estimator.
    Available model_name values:
      - "baseline_model" or "logistic_regression"
      - "random_forest"
    """
    if model_name in ("baseline_model", "logistic_regression"):
        model = LogisticRegression(**params)
    elif model_name == "random_forest":
        model = RandomForestClassifier(**params)
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")

    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test) -> dict:
    """
    Compute and return classification metrics.
    """
    y_pred = model.predict(X_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
    }


def save_model(model, path: Path) -> None:
    """
    Persist trained model to disk using joblib.
    """
    path_str = str(path)
    joblib.dump(model, path_str)
