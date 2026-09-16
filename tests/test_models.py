"""Real estimators, schema validation and deterministic splitting."""

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.core.models import create_classifier
from mlops_starter_kit.core.schemas import (
    validate_features,
    validate_training_table,
)
from mlops_starter_kit.io.datasets import train_test_split
from mlops_starter_kit.utils import train_model


@pytest.mark.parametrize(
    "name,expected",
    [
        ("logistic_regression", LogisticRegression),
        ("random_forest", RandomForestClassifier),
    ],
)
def test_model_names_fit_real_estimators(dataset, name, expected):
    table = pd.read_csv(dataset)
    model = train_model(
        table.drop(columns="target"), table.target.tolist(), name
    )
    assert isinstance(model, expected)
    assert (
        model.predict(table.drop(columns="target")).tolist()
        == table.target.tolist()
    )


def test_model_parameters_are_not_silently_ignored():
    with pytest.raises(TypeError):
        create_classifier("random_forest", unsupported_parameter=True)
    assert create_classifier("random_forest", n_estimators=7).n_estimators == 7


@pytest.mark.parametrize(
    "features",
    [
        pd.DataFrame({"a": []}),
        pd.DataFrame({"a": [float("nan")]}),
        pd.DataFrame({"a": [float("inf")]}),
        pd.DataFrame({"a": ["category"]}),
        pd.DataFrame([[1, 2]], columns=["a", "a"]),
    ],
)
def test_invalid_features_are_rejected(features):
    with pytest.raises(ValueError):
        validate_features(features)


def test_missing_target_and_null_target_are_rejected():
    with pytest.raises(ValueError, match="missing required"):
        validate_training_table(pd.DataFrame({"feature": [1]}))
    with pytest.raises(ValueError, match="target"):
        validate_training_table(
            pd.DataFrame({"feature": [1], "target": [None]})
        )


def test_split_is_reproducible_disjoint_and_stratified(dataset):
    table = pd.read_csv(dataset)
    first = train_test_split(table, "target", 0.25, 42)
    second = train_test_split(table, "target", 0.25, 42)
    pd.testing.assert_frame_equal(first[0], second[0])
    assert set(first[0].index).isdisjoint(first[1].index)
    assert len(first[0]) + len(first[1]) == len(table)
    assert set(first[2]) == set(first[3]) == {0, 1}


def test_too_small_dataset_fails_with_clear_message():
    with pytest.raises(ValueError, match="at least two"):
        train_test_split(pd.DataFrame({"x": [1], "target": [0]}), "target")


def test_multiclass_metrics_include_string_labels():
    metrics = classification_metrics(["a", "b", "c"], ["a", "b", "a"])
    assert metrics["accuracy"] == pytest.approx(2 / 3)
    assert 0 <= metrics["f1"] <= 1


@pytest.mark.parametrize("truth,prediction", [([], []), ([0], [0, 1])])
def test_invalid_metric_inputs_raise(truth, prediction):
    with pytest.raises(ValueError):
        classification_metrics(truth, prediction)
