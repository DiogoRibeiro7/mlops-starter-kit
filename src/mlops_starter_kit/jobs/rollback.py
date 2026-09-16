"""Restore an earlier model version with an audit reason."""

from mlops_starter_kit.core.configs import RollbackConfig
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.jobs.base import Job, Locals


class RollbackJob(Job[RollbackConfig]):
    kind = "rollback"
    config_type = RollbackConfig

    def run(self) -> Locals:
        config = self.config
        target = LocalModelRegistry(config.registry.path).rollback(
            config.rollback.alias, config.rollback.reason
        )
        return {"rollback": target, "reason": config.rollback.reason}
