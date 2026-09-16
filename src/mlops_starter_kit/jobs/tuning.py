"""Cross-validated parameter search using only the training partition."""

from mlops_starter_kit.core.configs import TuningConfig
from mlops_starter_kit.jobs.base import Job, Locals
from mlops_starter_kit.jobs.training import fit_and_register


class TuningJob(Job[TuningConfig]):
    kind = "tuning"
    config_type = TuningConfig

    def run(self) -> Locals:
        return fit_and_register(self.config, self.tracking, self.config.search)
