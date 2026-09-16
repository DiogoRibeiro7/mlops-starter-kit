"""Command line behavior outside the checkout, including clean failures."""

import json
from pathlib import Path
import subprocess
import sys

import pytest

from mlops_starter_kit.scripts import main


def test_installed_cli_runs_from_another_directory(training_config, tmp_path):
    config = tmp_path / "training.json"
    config.write_text(json.dumps(training_config))
    completed = subprocess.run(
        [sys.executable, "-m", "mlops_starter_kit", str(config)],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
    )
    result = json.loads(completed.stdout)
    assert isinstance(result["metrics"]["accuracy"], float)
    assert result["record"]["version"] == 1
    assert Path(result["model_path"]).exists()


def test_validate_has_no_artifact_side_effects(
    training_config, tmp_path, capsys
):
    config = tmp_path / "training.json"
    config.write_text(json.dumps(training_config))
    assert main([str(config), "--validate"]) == 0
    assert (
        json.loads(capsys.readouterr().out)["model"]["algorithm"]
        == "logistic_regression"
    )
    assert not (tmp_path / "artifacts").exists()


def test_schema_is_complete_json(capsys):
    assert main(["--schema"]) == 0
    schema = json.loads(capsys.readouterr().out)
    assert "training" in schema["schemas"]
    assert "dataset" in schema["schemas"]["training"]["properties"]


@pytest.mark.parametrize(
    "text",
    [
        '{"job":{"kind":"unknown"}}',
        '{"job":[]}',
        "{invalid",
    ],
)
def test_cli_reports_error_without_traceback(text, tmp_path, capsys):
    config = tmp_path / "invalid.json"
    config.write_text(text)
    assert main([str(config)]) == 1
    output = capsys.readouterr()
    assert "error:" in output.err
    assert "Traceback" not in output.err
    assert output.out == ""


def test_debug_preserves_traceback(tmp_path):
    with pytest.raises(FileNotFoundError):
        main([str(tmp_path / "missing.yaml"), "--debug"])
