from fastapi.testclient import TestClient
from mlops_starter_kit.api import app


def test_root_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Hello")
