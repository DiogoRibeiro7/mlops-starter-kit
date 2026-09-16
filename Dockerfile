FROM python:3.13-slim AS builder

WORKDIR /app
RUN python -m pip install --no-cache-dir poetry==2.2.1 \
    && python -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock README.md LICENSE ./
COPY src ./src
RUN poetry install --only main \
    && poetry build --format wheel \
    && python -m pip install --no-deps --force-reinstall dist/*.whl

FROM python:3.13-slim AS runtime
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --create-home app \
    && mkdir -p /app/artifacts \
    && chown -R app:app /app
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app confs ./confs
COPY --chown=app:app data/raw ./data/raw
USER app

FROM runtime AS train
ENTRYPOINT ["mlops-starter-kit"]
CMD ["confs/training.yaml"]

FROM runtime AS serve
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3)"
CMD ["uvicorn", "mlops_starter_kit.api:app", "--host", "0.0.0.0", "--port", "8000"]
