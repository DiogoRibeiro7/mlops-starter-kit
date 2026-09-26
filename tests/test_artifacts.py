"""Persistence failures, ingestion and provenance contracts."""

import json
import pickle

import numpy as np
import pandas as pd
from dataexcept import DataLoadingError, FileReadError, FileWriteError
import pytest

from mlops_starter_kit.data import ingest
from mlops_starter_kit.io.artifacts import (
    file_sha256,
    json_default,
    load_artifact,
    save_artifact,
    write_json,
)
from mlops_starter_kit.io.datasets import load_table
from mlops_starter_kit.io.provenance import (
    dataframe_fingerprint,
    write_fingerprint,
)


def test_invalid_json_does_not_replace_existing_metadata(tmp_path):
    path = tmp_path / "record.json"
    write_json(path, {"version": 1})
    with pytest.raises(ValueError):
        write_json(path, {"metric": float("nan")})
    assert json.loads(path.read_text()) == {"version": 1}
    assert not list(tmp_path.glob("*.tmp"))


def test_json_serializes_numpy_scalars_and_paths(tmp_path):
    path = tmp_path / "record.json"
    write_json(path, {"value": np.int64(7), "path": tmp_path})
    assert json.loads(path.read_text()) == {"value": 7, "path": str(tmp_path)}
    with pytest.raises(TypeError):
        json_default(object())


def test_wrong_artifact_format_requires_retraining(tmp_path):
    path = tmp_path / "legacy.pkl"
    path.write_bytes(pickle.dumps({"legacy": True}))
    with pytest.raises(ValueError, match="unsupported artifact"):
        load_artifact(path)


def test_provenance_changes_when_data_changes(tmp_path):
    table = pd.DataFrame({"feature": [1, 2], "target": [0, 1]})
    first = dataframe_fingerprint(table)
    assert first == dataframe_fingerprint(table.copy())
    table.loc[0, "feature"] = 99
    assert first != dataframe_fingerprint(table)
    path = tmp_path / "fingerprint.json"
    assert write_fingerprint(table, path) == dataframe_fingerprint(table)
    assert json.loads(path.read_text())["sha256"] == dataframe_fingerprint(
        table
    )


def test_ingestion_validates_and_creates_parent_directory(dataset, tmp_path):
    destination = tmp_path / "processed" / "data.csv"
    assert ingest(dataset, destination) == destination
    pd.testing.assert_frame_equal(
        pd.read_csv(dataset), pd.read_csv(destination)
    )
    invalid = tmp_path / "invalid.csv"
    invalid.write_text("feature\n1\n")
    with pytest.raises(ValueError):
        ingest(invalid, tmp_path / "invalid-output.csv")
    assert not (tmp_path / "invalid-output.csv").exists()


def test_csv_loading_identifies_missing_and_malformed_files(tmp_path):
    missing = tmp_path / "missing.csv"
    with pytest.raises(FileReadError) as error:
        load_table(missing)
    assert error.value.path == str(missing)
    assert isinstance(error.value.original, FileNotFoundError)
    assert error.value.__cause__ is error.value.original

    malformed = tmp_path / "malformed.csv"
    malformed.write_text('feature,target\n"unterminated,0\n')
    with pytest.raises(DataLoadingError) as error:
        load_table(malformed)
    assert error.value.source == str(malformed)
    assert isinstance(error.value.original, pd.errors.ParserError)
    assert error.value.__cause__ is error.value.original


def test_artifact_file_failures_keep_path_and_cause(tmp_path):
    missing = tmp_path / "missing.pkl"
    for load in (load_artifact, file_sha256):
        with pytest.raises(FileReadError) as error:
            load(missing)
        assert error.value.path == str(missing)
        assert isinstance(error.value.original, FileNotFoundError)
        assert error.value.__cause__ is error.value.original

    destination = tmp_path / "existing.pkl"
    destination.write_bytes(b"existing")
    with pytest.raises(FileWriteError) as error:
        save_artifact(object(), destination)
    assert error.value.path == str(destination)
    assert isinstance(error.value.original, FileExistsError)
    assert destination.read_bytes() == b"existing"


def test_atomic_metadata_write_failure_keeps_existing_data(tmp_path):
    destination = tmp_path / "existing-dir"
    destination.mkdir()
    with pytest.raises(FileWriteError) as error:
        write_json(destination, {"version": 1})
    assert error.value.path == str(destination)
    assert isinstance(error.value.original, OSError)
    assert error.value.__cause__ is error.value.original
    assert not list(tmp_path.glob("*.tmp"))


def test_ingest_write_failure_keeps_path_and_cause(dataset, tmp_path):
    destination = tmp_path / "existing-dir"
    destination.mkdir()
    with pytest.raises(FileWriteError) as error:
        ingest(dataset, destination)
    assert error.value.path == str(destination)
    assert isinstance(error.value.original, OSError)
