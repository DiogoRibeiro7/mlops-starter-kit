"""Example data ingestion script."""

from pathlib import Path
import pandas as pd

from mlops_starter_kit.config import RAW_DIR


def ingest(csv_path: Path) -> pd.DataFrame:
    """Load a CSV file and store it under RAW_DIR."""
    df = pd.read_csv(csv_path)
    destination = RAW_DIR / csv_path.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destination, index=False)
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ingest a CSV file")
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    ingest(args.csv_path)
    print(f"Ingested {args.csv_path} to {RAW_DIR}")

