"""Validate and ingest numeric classification CSV datasets."""

from pathlib import Path
from dataexcept import FileWriteError, wrapping

from mlops_starter_kit.core.schemas import validate_training_table
from mlops_starter_kit.io.datasets import load_table


def ingest(
    source: Path, destination: Path, target_column: str = "target"
) -> Path:
    """Validate a CSV and write a normalized copy to its destination."""
    table = validate_training_table(load_table(source), target_column)
    with wrapping(OSError, FileWriteError, path=str(destination)):
        destination.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(destination, index=False)
    return destination
