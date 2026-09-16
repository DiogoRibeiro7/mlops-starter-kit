"""A starter package for MLOps pipelines."""

from .main import main
from .config import get_config_and_logger
from .utils import (
    evaluate_model,
    load_data,
    save_model,
    split_data,
    train_model,
)
from .version import __version__

__all__ = [
    "__version__",
    "evaluate_model",
    "get_config_and_logger",
    "load_data",
    "main",
    "save_model",
    "split_data",
    "train_model",
]
