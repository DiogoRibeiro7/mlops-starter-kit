from __future__ import annotations
from typing import Any

class Response:
    def __init__(self, json_data: Any, status_code: int = 200) -> None:
        self._json = json_data
        self.status_code = status_code

    def json(self) -> Any:
        return self._json

class TestClient:
    __test__ = False  # avoid pytest collecting this class as a test

    def __init__(self, app) -> None:
        self.app = app

    def get(self, path: str) -> Response:
        func = self.app.routes.get(path)
        if func is None:
            return Response({"detail": "Not Found"}, status_code=404)
        data = func()
        return Response(data, status_code=200)
