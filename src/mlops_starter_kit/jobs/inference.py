"""Schema-checked batch predictions from a registered or local model."""

import pandas as pd

from mlops_starter_kit.core.configs import InferenceConfig
from mlops_starter_kit.io.datasets import load_table
from mlops_starter_kit.io.models import resolve_model
from mlops_starter_kit.jobs.base import Job, Locals


class InferenceJob(Job[InferenceConfig]):
    kind = "inference"
    config_type = InferenceConfig

    def run(self) -> Locals:
        model = resolve_model(self.config.model)
        predictions = model.predict(load_table(self.config.dataset.path))
        output_path = self.config.outputs.path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({"prediction": predictions}).to_csv(
            output_path, index=False
        )
        return {"predictions": predictions, "output_path": output_path}
