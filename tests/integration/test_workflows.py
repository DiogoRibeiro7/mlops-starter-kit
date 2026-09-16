"""Train through serving with real dataframes, estimators and artifacts."""

import json
from pathlib import Path

import pandas as pd
import pytest

from mlops_starter_kit.io.artifacts import load_artifact
from mlops_starter_kit.jobs import (
    EvaluationsJob,
    ExplanationsJob,
    InferenceJob,
    PromotionJob,
    RollbackJob,
    TrainingJob,
    TuningJob,
)


def run(job):
    with job:
        return job.run()


def test_complete_model_lifecycle(training_config, dataset, tmp_path):
    first = run(TrainingJob(training_config))
    second = run(TrainingJob(training_config))
    assert first["record"].version == 1
    assert second["record"].version == 2
    assert first["record"].path != second["record"].path
    reference = {
        "registry": str(tmp_path / "registry.json"),
        "name": "example",
    }
    config = {"dataset": {"path": str(dataset)}, "model": reference}
    evaluation = run(EvaluationsJob(config))
    assert evaluation["metrics"]["accuracy"] > 0.9
    predictions = run(
        InferenceJob(
            {
                **config,
                "outputs": {"path": str(tmp_path / "predictions.csv")},
            }
        )
    )
    assert len(predictions["predictions"]) == 24
    assert (
        pd.read_csv(predictions["output_path"]).prediction.tolist()
        == predictions["predictions"]
    )
    explanation = run(ExplanationsJob(config))
    assert len(explanation["explanation"]["features"]) == 2
    assert explanation["explanation"]["method"] == "permutation_importance"
    promotion = {
        "registry": {"path": str(tmp_path / "registry.json")},
        "model": {"name": "example", "version": 1},
        "promotion": {"min_accuracy": 0.75},
    }
    run(PromotionJob(promotion))
    promotion["model"]["version"] = 2
    run(PromotionJob(promotion))
    rollback = run(RollbackJob({"registry": promotion["registry"]}))
    assert rollback["rollback"] == {"name": "example", "version": 1}
    alias_predictions = run(
        InferenceJob(
            {
                "dataset": {"path": str(dataset)},
                "model": {
                    "registry": reference["registry"],
                    "alias": "champion",
                },
            }
        )
    )
    assert alias_predictions["predictions"] == predictions["predictions"]
    assert (
        load_artifact(first["model_path"]).algorithm == "logistic_regression"
    )


def test_tuning_uses_cross_validation_and_registers_winner(training_config):
    training_config["job"]["kind"] = "tuning"
    training_config["search"] = {"parameters": {"C": [0.1, 1.0]}, "folds": 3}
    result = run(TuningJob(training_config))
    assert result["best_params"]["C"] in {0.1, 1.0}
    assert 0 <= result["cv_accuracy"] <= 1
    assert result["model_path"].is_file()


def test_tuning_rejects_insufficient_class_support(training_config):
    training_config["job"]["kind"] = "tuning"
    training_config["search"] = {"folds": 100}
    with pytest.raises(ValueError, match="training class"):
        run(TuningJob(training_config))


def test_failed_run_is_recorded(training_config):
    training_config["dataset"]["path"] = "missing.csv"
    job = TrainingJob(training_config)
    with pytest.raises(FileNotFoundError):
        run(job)
    record = json.loads(job.tracking.path.read_text())
    assert record["status"] == "failed"
    assert record["error"]
    assert record["finished_at"]


def test_artifact_checksums_and_input_schema(training_config, dataset):
    result = run(TrainingJob(training_config))
    artifact = load_artifact(
        result["model_path"], result["record"].artifact_sha256
    )
    table = pd.read_csv(dataset)
    assert artifact.predict(table) == artifact.predict(
        table[["feature2", "feature1", "target"]]
    )
    with pytest.raises(ValueError, match="expected feature"):
        artifact.predict(table.drop(columns="feature1"))
    with pytest.raises(ValueError, match="checksum"):
        load_artifact(result["model_path"], "incorrect")


def test_unique_tracking_records(training_config):
    first, second = TrainingJob(training_config), TrainingJob(training_config)
    run(first)
    run(second)
    assert first.tracking.path != second.tracking.path
    state = json.loads(first.tracking.path.read_text())
    assert state["status"] == "completed"
    assert state["config"]["model"]["algorithm"] == "logistic_regression"
    assert state["metrics"]["accuracy"] >= 0.5
    assert (
        len(
            list(Path(training_config["tracking"]["directory"]).glob("*.json"))
        )
        == 2
    )
