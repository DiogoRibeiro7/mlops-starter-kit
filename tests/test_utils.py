import pandas as pd
from pathlib import Path
from mlops_starter_kit import utils


def test_load_data(tmp_path: Path) -> None:
    csv = tmp_path / "tmp.csv"
    csv.write_text("a,b,target\n1,2,0\n3,4,1\n")
    df = utils.load_data(csv)
    assert list(df.columns) == ["a", "b", "target"]
    assert len(df) == 2


def test_split_data() -> None:
    df = pd.DataFrame({"f1": [1, 2, 3], "target": [0, 1, 0]})
    X_train, X_test, y_train, y_test = utils.split_data(df, "target", test_size=0.33, random_state=0)
    assert len(X_train) == 2
    assert len(X_test) == 1
    assert len(y_train) == 2
    assert len(y_test) == 1


def test_train_model_and_evaluate() -> None:
    df = pd.DataFrame({"f1": [1, 2, 3, 4], "target": [0, 1, 0, 1]})
    X_train, X_test, y_train, y_test = utils.split_data(df, "target", test_size=0.5, random_state=0)
    model = utils.train_model(X_train, y_train, model_name="logistic_regression", max_iter=10)
    metrics = utils.evaluate_model(model, X_test, y_test)
    assert set(metrics) == {"accuracy", "precision", "recall", "f1"}


def test_train_model_invalid() -> None:
    df = pd.DataFrame({"f": [1, 2], "target": [0, 1]})
    X_train, X_test, y_train, y_test = utils.split_data(df, "target")
    try:
        utils.train_model(X_train, y_train, model_name="does_not_exist")
    except ValueError as e:
        assert "Unsupported" in str(e)
    else:
        assert False, "ValueError not raised"


def test_save_model(tmp_path: Path) -> None:
    df = pd.DataFrame({"f": [1, 2], "target": [0, 1]})
    X_train, _, y_train, _ = utils.split_data(df, "target")
    model = utils.train_model(X_train, y_train)
    path = tmp_path / "model.pkl"
    utils.save_model(model, path)
    assert path.exists()
