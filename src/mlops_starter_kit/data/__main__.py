"""Command line dataset ingestion."""

import argparse
from pathlib import Path

from mlops_starter_kit.data import ingest


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and ingest a CSV")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--target-column", default="target")
    args = parser.parse_args()
    print(ingest(args.source, args.destination, args.target_column))


if __name__ == "__main__":
    main()
