# src/mlops_starter_kit/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from omegaconf import OmegaConf, DictConfig
import logging.config

# 1. Load .env file (if present)
ENV_PATH = Path(__file__).parents[2] / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

def load_config(config_path: str = None) -> DictConfig:
    """
    Load the main Hydra/OmegaConf configuration.
    Defaults to configs/config.yaml at the project root.
    """
    if config_path is None:
        # relative to project root
        config_path = Path(__file__).parents[2] / "configs" / "config.yaml"
    cfg = OmegaConf.load(str(config_path))
    return cfg

def setup_logging(logging_cfg_path: str = None) -> None:
    """
    Configure Python logging from a YAML file.
    Defaults to configs/logging.yaml at the project root.
    """
    if logging_cfg_path is None:
        logging_cfg_path = Path(__file__).parents[2] / "configs" / "logging.yaml"
    logging_cfg = OmegaConf.load(str(logging_cfg_path))
    # OmegaConf.load returns a DictConfig; convert to plain dict
    logging.config.dictConfig(OmegaConf.to_container(logging_cfg, resolve=True))

def get_config_and_logger() -> DictConfig:
    """
    Convenience function: loads config, sets up logging, returns config.
    """
    cfg = load_config()
    setup_logging()
    logging.getLogger(__name__).info("Configuration and logging are set up.")
    return cfg

