"""Configuration parsing and validation at the public job boundary."""

import json

import pytest
from pydantic import ValidationError

from mlops_starter_kit.core.configs import ModelReference, TrainingConfig
from mlops_starter_kit.io.configs import load_config_file, merge_dicts
from mlops_starter_kit.jobs.training import TrainingJob
from mlops_starter_kit.scripts import job_from_config


def test_yaml_preserves_quotes_lists_and_comments(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text('name: "a#b:c"\nvalues: [1, 2, 3] # note\nflag: true\n')
    assert load_config_file(path) == {
        "name": "a#b:c",
        "values": [1, 2, 3],
        "flag": True,
    }


@pytest.mark.parametrize(
    "text", ["[]", "null", "hello", "[broken", "1: value"]
)
def test_rejects_invalid_config_mapping(tmp_path, text):
    path = tmp_path / "config.yaml"
    path.write_text(text)
    with pytest.raises(ValueError):
        load_config_file(path)


def test_json_and_yaml_have_equivalent_values(tmp_path):
    path = tmp_path / "config.json"
    data = {"job": {"kind": "training"}, "dataset": {"test_size": 0.3}}
    path.write_text(json.dumps(data))
    assert job_from_config(path).config.dataset.test_size == 0.3


@pytest.mark.parametrize(
    "config",
    [
        {"dataset": {"test_size": 1}},
        {"dataset": {"random_seed": -1}},
        {"modle": {}},
        {"model": {"name": "../outside"}},
        {"model": {"algorithm": "missing"}},
    ],
)
def test_invalid_job_configuration_fails_before_writes(tmp_path, config):
    with pytest.raises(ValidationError):
        TrainingJob(config)
    assert not (tmp_path / "artifacts").exists()


def test_job_kind_mismatch_is_rejected():
    with pytest.raises(ValueError, match="expected job kind"):
        TrainingJob({"job": {"kind": "rollback"}})


def test_defaults_are_independent():
    first, second = TrainingConfig(), TrainingConfig()
    first.model.parameters["max_iter"] = 7
    assert second.model.parameters == {}
    source = {"a": {"values": [1]}}
    merged = merge_dicts(source, {})
    merged["a"]["values"].append(2)
    assert source == {"a": {"values": [1]}}


@pytest.mark.parametrize(
    "selector",
    [
        {"path": "model.pkl", "alias": "champion"},
        {"alias": "champion", "version": 1},
        {"version": 0},
    ],
)
def test_ambiguous_model_reference_is_rejected(selector):
    with pytest.raises(ValueError):
        ModelReference(**selector)


def test_unsafe_yaml_tag_is_rejected(tmp_path):
    path = tmp_path / "unsafe.yaml"
    path.write_text("!!python/object/apply:builtins.str [hello]")
    with pytest.raises(ValueError):
        load_config_file(path)
