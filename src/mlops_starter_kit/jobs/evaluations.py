"""Evaluate a trusted artifact against a labelled dataset."""

from mlops_starter_kit.core.configs import EvaluationConfig
from mlops_starter_kit.core.metrics import classification_metrics
from mlops_starter_kit.io.datasets import load_table, split_features_target
from mlops_starter_kit.io.models import resolve_model
from mlops_starter_kit.jobs.base import Job, Locals


class EvaluationsJob(Job[EvaluationConfig]):
    kind = "evaluations"
    config_type = EvaluationConfig

    def run(self) -> Locals:
        artifact = resolve_model(self.config.model)
        table = load_table(self.config.dataset.path)
        features, target = split_features_target(
            table, self.config.dataset.target_column
        )
        metrics = classification_metrics(target, artifact.predict(features))
        self.tracking.log_metrics(metrics)
        return {"metrics": metrics, "run_id": self.tracking.run_id}
