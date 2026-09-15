FROM python:3.10-slim AS train

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN python -m pip install --no-cache-dir .

COPY confs ./confs
COPY data/raw ./data/raw

ENTRYPOINT ["mlops-starter-kit"]
CMD ["confs/training.yaml"]
