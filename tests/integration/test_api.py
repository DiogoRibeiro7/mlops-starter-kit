"""HTTP validation using the real FastAPI application and ASGI lifecycle."""

from fastapi.testclient import TestClient
import pytest

from mlops_starter_kit.api import create_app
from mlops_starter_kit.core.configs import ModelReference
from mlops_starter_kit.jobs.training import TrainingJob


@pytest.fixture
def trained_reference(training_config):
    with TrainingJob(training_config) as job:
        result = job.run()
    return ModelReference(path=result["model_path"])


def test_health_and_readiness_without_model():
    with TestClient(create_app()) as client:
        assert client.get("/").json()["message"].startswith("Hello")
        assert client.get("/healthz").json() == {"status": "ok"}
        assert client.get("/readyz").status_code == 503
        assert (
            client.post(
                "/predict", json={"instances": [{"feature1": 1}]}
            ).status_code
            == 503
        )


def test_prediction_and_readiness(trained_reference):
    with TestClient(create_app(trained_reference)) as client:
        assert client.get("/readyz").status_code == 200
        response = client.post(
            "/predict",
            json={
                "instances": [
                    {"feature1": 0, "feature2": 0},
                    {"feature1": 23, "feature2": 11.5},
                ]
            },
        )
        assert response.status_code == 200
        assert response.json()["predictions"] == [0, 1]


@pytest.mark.parametrize(
    "payload",
    [
        {"instances": []},
        {"instances": [{"wrong": 1}]},
        {"instances": [{"feature1": "not numeric", "feature2": 1}]},
        {"instances": [{"feature1": 1, "feature2": 1}], "unknown": True},
        {"instances": [{"feature1": 1, "feature2": 1}] * 1001},
    ],
)
def test_invalid_prediction_inputs_return_422(trained_reference, payload):
    with TestClient(create_app(trained_reference)) as client:
        assert client.post("/predict", json=payload).status_code == 422


def test_model_path_environment_is_loaded(trained_reference, monkeypatch):
    monkeypatch.setenv("MODEL_PATH", str(trained_reference.path))
    with TestClient(create_app()) as client:
        assert client.get("/readyz").status_code == 200
