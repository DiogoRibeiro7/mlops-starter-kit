"""Configuration helpers for the example project.

These versions avoid optional third-party dependencies so the unit
tests remain lightweight.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).parents[2]
RAW_DIR = Path(os.getenv("RAW_DIR", PROJECT_ROOT / "data" / "raw"))
PROCESSED_DIR = Path(os.getenv("PROCESSED_DIR", PROJECT_ROOT / "data" / "processed"))


def load_config(config_path: str | None = None) -> SimpleNamespace:
    """Load configuration.

    The example implementation returns a small object with the project name.
    """
    return SimpleNamespace(project=SimpleNamespace(name="mlops-starter"))


def setup_logging(logging_cfg_path: str | None = None) -> None:
    """Configure basic logging."""
    logging.basicConfig(level=logging.INFO, force=True)


def get_config_and_logger() -> SimpleNamespace:
    """Return configuration and ensure logging is configured."""
    cfg = load_config()
    setup_logging()
    logging.getLogger(__name__).info("Configuration and logging are set up.")
    return cfg
