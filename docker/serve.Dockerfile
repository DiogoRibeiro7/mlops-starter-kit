# GPU inference base stage
FROM nvidia/cuda:11.8.0-runtime-ubuntu20.04 AS gpu-serve

RUN apt-get update && apt-get install -y \
    python3.10 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN pip3 install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && pip3 install --no-cache-dir torch torchvision --extra-index-url https://download.pytorch.org/whl/cu118

COPY src/ /app/src/

EXPOSE 8000
CMD ["uvicorn", "src.mlops_starter_kit.api:app", "--host", "0.0.0.0", "--port", "8000"]
