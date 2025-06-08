"""
mlops_starter_kit
A starter package for MLOps pipelines.
"""

# Core entrypoint
from .main import main

# Config & logging
from .config import get_config_and_logger

# Pipeline utilities
from .utils import (
    load_data,
    split_data,
    train_model,
    evaluate_model,
    save_model,
)

__all__ = [
    "main",
    "get_config_and_logger",
    "load_data",
    "split_data",
    "train_model",
    "evaluate_model",
    "save_model",
]
