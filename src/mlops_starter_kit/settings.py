"""Project-wide paths and defaults."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_NAME = "mlops_starter_kit"
PROJECT_NAME = "mlops-starter-kit"
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = Path(os.getenv("DATA_DIR", PROJECT_ROOT / "data"))
RAW_DIR = Path(os.getenv("RAW_DIR", DATA_DIR / "raw"))
PROCESSED_DIR = Path(os.getenv("PROCESSED_DIR", DATA_DIR / "processed"))
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", PROJECT_ROOT / "artifacts"))
CONFIGS_DIR = Path(os.getenv("CONFIGS_DIR", PROJECT_ROOT / "confs"))
