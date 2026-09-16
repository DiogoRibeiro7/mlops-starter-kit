"""Permutation feature importance against a labelled evaluation table."""

from sklearn.inspection import permutation_importance

from mlops_starter_kit.core.configs import ExplanationConfig
from mlops_starter_kit.io.artifacts import write_json
from mlops_starter_kit.io.datasets import load_table, split_features_target
from mlops_starter_kit.io.models import resolve_model
from mlops_starter_kit.jobs.base import Job, Locals


class ExplanationsJob(Job[ExplanationConfig]):
    kind = "explanations"
    config_type = ExplanationConfig

    def run(self) -> Locals:
        artifact = resolve_model(self.config.model)
        features, target = split_features_target(
            load_table(self.config.dataset.path),
            self.config.dataset.target_column,
        )
        importance = permutation_importance(
            artifact.estimator,
            artifact.prepare(features),
            target,
            scoring="accuracy",
            n_repeats=self.config.repeats,
            random_state=self.config.dataset.random_seed,
            n_jobs=1,
        )
        explanation = {
            "method": "permutation_importance",
            "scoring": "accuracy",
            "features": [
                {"name": name, "mean": float(mean), "std": float(std)}
                for name, mean, std in zip(
                    artifact.features,
                    importance.importances_mean,
                    importance.importances_std,
                )
            ],
        }
        write_json(self.config.outputs.path, explanation)
        return {
            "explanation": explanation,
            "output_path": self.config.outputs.path,
        }
