# Base stage with Python runtime and common dependencies
FROM python:3.10-slim AS base

WORKDIR /app

# Install system packages and Python dependencies
RUN apt-get update && apt-get install -y \
    build-essential git \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# GPU-enabled base stage
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04 AS gpu-base

# Install Python and system deps
RUN apt-get update && apt-get install -y \
    python3.10 python3-pip python3-dev \
    build-essential git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip3 install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Install GPU-specific ML libraries
RUN pip3 install --no-cache-dir torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118

# Final stage: copy runtime
FROM base AS train

# Copy Python packages from GPU base
COPY --from=gpu-base /usr/local/lib/python3.10/dist-packages/ /usr/local/lib/python3.10/dist-packages/

COPY src/ /app/src/
WORKDIR /app

ENTRYPOINT ["python3", "-m", "src.mlops_starter_kit.modeling.train"]
