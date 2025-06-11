"""Extremely small FastAPI stub for testing."""
from __future__ import annotations
from typing import Callable, Dict, Any

class FastAPI:
    def __init__(self) -> None:
        self.routes: Dict[str, Callable[[], Any]] = {}

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.routes[path] = func
            return func
        return decorator

from .testclient import TestClient  # re-export for convenience
