"""Compatibility helpers for earlier environment-based scripts."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from types import SimpleNamespace

from dotenv import load_dotenv

from mlops_starter_kit.settings import PROCESSED_DIR, PROJECT_ROOT, RAW_DIR

__all__ = [
    "PROCESSED_DIR",
    "PROJECT_ROOT",
    "RAW_DIR",
    "get_config_and_logger",
    "load_config",
    "load_env",
    "setup_logging",
]


def load_env(path: str | os.PathLike = ".env") -> None:
    """Load key=value pairs from an ``.env`` file into ``os.environ``.

    Existing variables are not overwritten. Lines starting with ``#`` are
    ignored.
    """
    load_dotenv(Path(path), override=False)


def load_config(config_path: str | None = None) -> SimpleNamespace:
    """Load configuration.

    Environment variables and an optional ``.env`` file are parsed to populate
    basic fields used throughout the example pipeline.
    """
    load_env()

    project_name = os.getenv("PROJECT_NAME", "mlops-starter")
    dataset_path = os.getenv("DATASET_PATH", str(RAW_DIR))
    dataset_filename = os.getenv("DATASET_FILENAME", "example.csv")

    cfg = SimpleNamespace(
        project=SimpleNamespace(name=project_name),
        dataset=SimpleNamespace(
            path=dataset_path,
            filename=dataset_filename,
            target_col=os.getenv("TARGET_COL", "target"),
            test_size=float(os.getenv("TEST_SIZE", "0.2")),
            random_seed=int(os.getenv("RANDOM_SEED", "42")),
        ),
        model=SimpleNamespace(
            name=os.getenv("MODEL_NAME", "baseline_model"),
            params={},
            artifact_dir=os.getenv("ARTIFACT_DIR", "artifacts"),
        ),
    )

    return cfg


def setup_logging(logging_cfg_path: str | None = None) -> None:
    """Configure basic logging."""
    logging.basicConfig(level=logging.INFO, force=True)


def get_config_and_logger() -> SimpleNamespace:
    """Return configuration and ensure logging is configured."""
    cfg = load_config()
    setup_logging()
    logging.getLogger(__name__).info("Configuration and logging are set up.")
    return cfg
