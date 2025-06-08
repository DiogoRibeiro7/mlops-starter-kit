# Base image for training and serving stages
FROM python:3.10-slim AS base

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
  && rm -rf /var/lib/apt/lists/*

# Copy project files and install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev
