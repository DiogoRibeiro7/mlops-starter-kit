"""Prediction service for an explicitly configured trusted model artifact."""

from contextlib import asynccontextmanager
import os
from pathlib import Path
from typing import Any, AsyncIterator

from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, FiniteFloat

from mlops_starter_kit.version import __version__
from mlops_starter_kit.core.configs import ModelReference
from mlops_starter_kit.io.models import resolve_model


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    instances: list[dict[str, FiniteFloat]] = Field(
        min_length=1, max_length=1000
    )


class PredictionResponse(BaseModel):
    predictions: list[int | float | str]


def create_app(reference: ModelReference | None = None) -> FastAPI:
    """Create an app whose model is loaded once during startup."""
    if reference is None and os.getenv("MODEL_PATH"):
        reference = ModelReference(path=Path(os.environ["MODEL_PATH"]))

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.model = (
            resolve_model(reference) if reference else None
        )
        yield

    application = FastAPI(
        title="MLOps Starter Kit",
        version=__version__,
        lifespan=lifespan,
    )

    @application.get("/")
    def root() -> dict[str, str]:
        return {
            "message": "Hello from mlops-starter-kit",
            "version": __version__,
        }

    @application.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/readyz")
    def readiness() -> dict[str, str]:
        if application.state.model is None:
            raise HTTPException(503, "No model configured")
        return {"status": "ready"}

    @application.post("/predict", response_model=PredictionResponse)
    def predict(payload: PredictionRequest) -> Any:
        if application.state.model is None:
            raise HTTPException(503, "No model configured")
        try:
            predictions = application.state.model.predict(
                pd.DataFrame(payload.instances)
            )
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc
        return {"predictions": predictions}

    return application


app = create_app()
