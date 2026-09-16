"""Promote an intact registered version after an explicit quality gate."""

from mlops_starter_kit.core.configs import PromotionConfig
from mlops_starter_kit.io.registries import LocalModelRegistry
from mlops_starter_kit.jobs.base import Job, Locals


class PromotionJob(Job[PromotionConfig]):
    kind = "promotion"
    config_type = PromotionConfig

    def run(self) -> Locals:
        config = self.config
        result = LocalModelRegistry(config.registry.path).promote(
            config.model.name,
            config.model.version,
            config.promotion.alias,
            config.promotion.min_accuracy,
        )
        return {"promotion": result}
