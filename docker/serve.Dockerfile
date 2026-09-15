FROM python:3.10-slim AS serve

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "mlops_starter_kit.api:app", "--host", "0.0.0.0", "--port", "8000"]
