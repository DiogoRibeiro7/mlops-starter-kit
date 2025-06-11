#!/usr/bin/env bash
# Simple script to start the FastAPI app with uvicorn
uvicorn mlops_starter_kit.api:app --host 0.0.0.0 --port 8000
