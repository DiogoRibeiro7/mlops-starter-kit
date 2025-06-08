"""Minimal FastAPI application."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint returning a welcome message."""
    return {"message": "Hello from mlops-starter-kit"}
