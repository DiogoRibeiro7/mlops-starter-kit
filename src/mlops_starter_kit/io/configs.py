"""Load structured configuration without executing YAML tags."""

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import yaml


def load_config_file(path: str | Path) -> dict[str, Any]:
    """Read a JSON or YAML mapping; paths inside it are relative to cwd."""
    config_path = Path(path)
    text = config_path.read_text(encoding="utf-8")
    try:
        config = (
            json.loads(text)
            if config_path.suffix.lower() == ".json"
            else yaml.safe_load(text)
        )
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ValueError(
            f"invalid configuration in {config_path}: {exc}"
        ) from exc
    if not isinstance(config, dict) or not all(
        isinstance(key, str) for key in config
    ):
        raise ValueError("configuration must be a mapping with string keys")
    return config


def merge_dicts(
    base: dict[str, Any], override: dict[str, Any]
) -> dict[str, Any]:
    """Merge configuration values without sharing nested mutable defaults."""
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def load_job_config(
    path: str | Path, defaults: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Load configuration with optional recursive defaults."""
    return merge_dicts(defaults or {}, load_config_file(path))
