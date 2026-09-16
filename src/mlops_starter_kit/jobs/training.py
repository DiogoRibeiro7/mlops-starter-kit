"""Train, evaluate on a held-out split and register an immutable model."""

from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.model_selection import GridSearchCV, StratifiedKFold

from mlops_starter_kit.core.configs import SearchConfig, TrainingConfig
from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.core.models import ModelArtifact, create_classifier
from mlops_starter_kit.io.artifacts import save_artifact, write_json
from mlops_starter_kit.io.datasets import load_table, train_test_split
from mlops_starter_kit.io.provenance import dataframe_fingerprint
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.io.services import LocalTrackingService
from mlops_starter_kit.jobs.base import Job, Locals


def fit_and_register(
    config: TrainingConfig,
    tracking: LocalTrackingService,
    search: SearchConfig | None = None,
) -> Locals:
    table = load_table(config.dataset.path)
    x_train, x_test, y_train, y_test = train_test_split(
        table,
        config.dataset.target_column,
        config.dataset.test_size,
        config.dataset.random_seed,
    )
    estimator = create_classifier(
        config.model.algorithm,
        config.dataset.random_seed,
        **config.model.parameters,
    )
    search_result: dict[str, Any] = {}
    if search is not None:
        counts = pd.Series(y_train).value_counts()
        if len(counts) < 2 or counts.min() < search.folds:
            raise ValueError(
                "each training class needs at least search.folds rows"
            )
        cv = StratifiedKFold(
            n_splits=search.folds,
            shuffle=True,
            random_state=config.dataset.random_seed,
        )
        candidates = GridSearchCV(
            estimator,
            search.parameters,
            scoring="accuracy",
            cv=cv,
            error_score="raise",
            n_jobs=1,
        ).fit(x_train, y_train)
        estimator = candidates.best_estimator_
        search_result = {
            "best_params": candidates.best_params_,
            "cv_accuracy": float(candidates.best_score_),
        }
    else:
        estimator.fit(x_train, y_train)
    artifact = ModelArtifact(
        estimator,
        tuple(x_train.columns),
        config.dataset.target_column,
        config.model.algorithm,
    )
    metrics = classification_metrics(y_test, artifact.predict(x_test))
    run_directory = config.artifacts.directory / "runs" / tracking.run_id
    model_path = run_directory / "model.pkl"
    save_artifact(artifact, model_path)
    fingerprint = dataframe_fingerprint(table)
    metadata = {
        "run_id": tracking.run_id,
        "dataset_sha256": fingerprint,
        "training_rows": len(x_train),
        "evaluation_rows": len(x_test),
        "features": list(artifact.features),
        "metrics": metrics,
        "config": config.model_dump(mode="json"),
        **search_result,
    }
    write_json(run_directory / "metadata.json", metadata)
    record = LocalModelRegistry(config.artifacts.registry).register(
        config.model.name,
        model_path,
        metrics,
        fingerprint,
    )
    tracking.log_metrics(metrics)
    return {
        "metrics": metrics,
        "record": record,
        "model_path": Path(record.path),
        "run_id": tracking.run_id,
        **search_result,
    }


class TrainingJob(Job[TrainingConfig]):
    kind = "training"
    config_type = TrainingConfig

    def run(self) -> Locals:
        return fit_and_register(self.config, self.tracking)
