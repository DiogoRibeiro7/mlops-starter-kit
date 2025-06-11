"""Minimal stub of the pandas API used in tests."""
from __future__ import annotations
import csv
import os
from typing import Dict, List, Iterable, Any

class DataFrame:
    def __init__(self, data: Dict[str, Iterable[Any]]):
        self._data = {k: list(v) for k, v in data.items()}
        self.columns = list(data.keys())

    def __len__(self) -> int:  # number of rows
        if not self.columns:
            return 0
        first = self.columns[0]
        return len(self._data[first])

    def __getitem__(self, key: str) -> List[Any]:
        return self._data[key]

    def drop(self, columns: Iterable[str]) -> "DataFrame":
        if isinstance(columns, str):
            columns = [columns]
        new_data = {k: v for k, v in self._data.items() if k not in columns}
        return DataFrame(new_data)

def read_csv(path: str | bytes | os.PathLike) -> DataFrame:
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        data: Dict[str, List[Any]] = {field: [] for field in reader.fieldnames or []}
        for row in reader:
            for k, v in row.items():
                try:
                    val = int(v)
                except ValueError:
                    try:
                        val = float(v)
                    except ValueError:
                        val = v
                data[k].append(val)
    return DataFrame(data)
