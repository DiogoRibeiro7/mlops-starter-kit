"""Validate and ingest numeric classification CSV datasets."""

from pathlib import Path

import pandas as pd

from mlops_starter_kit.core.schemas import validate_training_table


def ingest(
    source: Path, destination: Path, target_column: str = "target"
) -> Path:
    """Validate a CSV and write a normalized copy to its destination."""
    table = validate_training_table(pd.read_csv(source), target_column)
    destination.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(destination, index=False)
    return destination
