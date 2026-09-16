"""Validated configuration contracts shared by the CLI and jobs."""

from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Name = Annotated[str, Field(pattern=r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")]
Algorithm = Literal["baseline_model", "logistic_regression", "random_forest"]


class ConfigModel(BaseModel):
    """Reject misspelled configuration keys."""

    model_config = ConfigDict(extra="forbid", validate_default=True)


class JobSpec(ConfigModel):
    kind: Literal[
        "training",
        "evaluations",
        "inference",
        "tuning",
        "explanations",
        "promotion",
        "rollback",
    ]


class TrackingConfig(ConfigModel):
    directory: Path = Field(default_factory=lambda: Path("artifacts/tracking"))


class JobConfig(ConfigModel):
    job: JobSpec
    tracking: TrackingConfig = Field(default_factory=TrackingConfig)


class DatasetConfig(ConfigModel):
    path: Path = Field(default_factory=lambda: Path("data/raw/example.csv"))
    target_column: str = Field(default="target", min_length=1)
    test_size: float = Field(default=0.2, gt=0, lt=1)
    random_seed: int = Field(default=42, ge=0)


class ModelConfig(ConfigModel):
    name: Name = "baseline_model"
    algorithm: Algorithm = "baseline_model"
    parameters: dict[str, Any] = Field(default_factory=dict)


class ArtifactsConfig(ConfigModel):
    directory: Path = Field(default_factory=lambda: Path("artifacts"))
    registry: Path = Field(
        default_factory=lambda: Path("artifacts/registry.json")
    )


class TrainingConfig(JobConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="training"))
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    artifacts: ArtifactsConfig = Field(default_factory=ArtifactsConfig)


class ModelReference(ConfigModel):
    path: Path | None = None
    registry: Path = Field(
        default_factory=lambda: Path("artifacts/registry.json")
    )
    name: Name = "baseline_model"
    version: int | None = Field(default=None, ge=1)
    alias: Name | None = None

    @model_validator(mode="after")
    def exclusive_selector(self) -> "ModelReference":
        if self.path is not None and (
            self.alias is not None or self.version is not None
        ):
            raise ValueError(
                "model.path cannot be combined with alias/version"
            )
        if self.alias is not None and self.version is not None:
            raise ValueError("choose either model.alias or model.version")
        return self


class EvaluationConfig(JobConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="evaluations"))
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    model: ModelReference = Field(default_factory=ModelReference)


class OutputConfig(ConfigModel):
    path: Path


class InferenceConfig(EvaluationConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="inference"))
    outputs: OutputConfig = Field(
        default_factory=lambda: OutputConfig(
            path=Path("artifacts/predictions.csv")
        )
    )


class SearchConfig(ConfigModel):
    parameters: dict[str, list[Any]] = Field(
        default_factory=lambda: {"C": [0.1, 1.0, 10.0]}
    )
    folds: int = Field(default=3, ge=2)


class TuningConfig(TrainingConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="tuning"))
    model: ModelConfig = Field(
        default_factory=lambda: ModelConfig(algorithm="logistic_regression")
    )
    search: SearchConfig = Field(default_factory=SearchConfig)


class ExplanationConfig(EvaluationConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="explanations"))
    repeats: int = Field(default=5, ge=1, le=100)
    outputs: OutputConfig = Field(
        default_factory=lambda: OutputConfig(
            path=Path("artifacts/explanations.json")
        )
    )


class RegistryConfig(ConfigModel):
    path: Path = Field(default_factory=lambda: Path("artifacts/registry.json"))


class VersionConfig(ConfigModel):
    name: Name = "baseline_model"
    version: int = Field(default=1, ge=1)


class PromotionPolicy(ConfigModel):
    alias: Name = "champion"
    min_accuracy: float = Field(default=0.0, ge=0, le=1)


class PromotionConfig(JobConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="promotion"))
    registry: RegistryConfig = Field(default_factory=RegistryConfig)
    model: VersionConfig = Field(default_factory=VersionConfig)
    promotion: PromotionPolicy = Field(default_factory=PromotionPolicy)


class RollbackPolicy(ConfigModel):
    alias: Name = "champion"
    reason: str = Field(default="manual rollback", min_length=1)


class RollbackConfig(JobConfig):
    job: JobSpec = Field(default_factory=lambda: JobSpec(kind="rollback"))
    registry: RegistryConfig = Field(default_factory=RegistryConfig)
    rollback: RollbackPolicy = Field(default_factory=RollbackPolicy)
