"""Configuration helpers for the example project.

These versions avoid optional third-party dependencies so the unit
tests remain lightweight.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from types import SimpleNamespace


def load_env(path: str | os.PathLike = ".env") -> None:
    """Load key=value pairs from an ``.env`` file into ``os.environ``.

    Existing variables are not overwritten. Lines starting with ``#`` are
    ignored.
    """
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


PROJECT_ROOT = Path(__file__).parents[2]
RAW_DIR = Path(os.getenv("RAW_DIR", PROJECT_ROOT / "data" / "raw"))
PROCESSED_DIR = Path(
    os.getenv("PROCESSED_DIR", PROJECT_ROOT / "data" / "processed")
)


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
