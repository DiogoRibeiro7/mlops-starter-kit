"""Example data ingestion script."""

from pathlib import Path
import pandas as pd

from mlops_starter_kit.config import RAW_DIR
from mlops_starter_kit.data import ingest as ingest_dataset


def ingest(csv_path: Path) -> pd.DataFrame:
    """Load a CSV file and store it under RAW_DIR."""
    destination = RAW_DIR / csv_path.name
    ingest_dataset(csv_path, destination)
    return pd.read_csv(destination)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest a CSV file")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    ingest(args.csv_path)
    print(f"Ingested {args.csv_path} to {RAW_DIR}")
