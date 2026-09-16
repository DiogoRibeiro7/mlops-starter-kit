"""Dataset split helpers."""

from __future__ import annotations

from typing import Sequence, TypeVar

T = TypeVar("T")


def chronological_split(
    items: Sequence[T], test_size: int
) -> tuple[list[T], list[T]]:
    """Split a sequence without shuffling, preserving temporal order."""
    if test_size <= 0:
        raise ValueError("test_size must be positive")
    if test_size >= len(items):
        raise ValueError("test_size must be smaller than the sequence length")
    return list(items[:-test_size]), list(items[-test_size:])
