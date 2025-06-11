import logging
from mlops_starter_kit import config


def test_load_config() -> None:
    cfg = config.load_config()
    assert cfg.project.name == "mlops-starter"


def test_setup_logging(tmp_path) -> None:
    cfg_path = tmp_path / "logging.yaml"
    cfg_path.write_text("version: 1\nroot:\n  level: INFO\n  handlers: []\n")
    config.setup_logging(str(cfg_path))
    assert logging.getLogger().level == logging.INFO


def test_get_config_and_logger() -> None:
    cfg = config.get_config_and_logger()
    assert cfg.project.name == "mlops-starter"
    assert logging.getLogger().handlers

