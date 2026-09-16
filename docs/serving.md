# Prediction API

## Start Locally

First [train a model](quickstart.md#train-and-predict), then configure its path.
Use the actual version path when selecting a model other than the first run.

=== "Bash"

    ```bash
    export MODEL_PATH=artifacts/models/baseline_model/v1.pkl
    poetry run uvicorn mlops_starter_kit.api:app --host 127.0.0.1 --port 8000
    ```

=== "PowerShell"

    ```powershell
    $env:MODEL_PATH = "artifacts/models/baseline_model/v1.pkl"
    poetry run uvicorn mlops_starter_kit.api:app --host 127.0.0.1 --port 8000
    ```

The model loads once at startup. Changing an alias or file does not hot-reload
the running process; restart the service to load the selected version.

## Endpoints

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/healthz` | Process liveness, independent of model availability |
| GET | `/readyz` | Ready when a model is loaded; otherwise HTTP 503 |
| POST | `/predict` | Predictions for finite numeric feature records |
| GET | `/docs` | Interactive OpenAPI documentation |

Prediction requests may contain up to 1,000 records. Missing, extra or invalid
features return HTTP 422. Without a configured model, prediction returns HTTP
503. Input feature order is restored from the trained artifact.

=== "Bash"

    ```bash
    curl --fail http://127.0.0.1:8000/predict \
      -H 'Content-Type: application/json' \
      -d '{"instances":[{"feature1":1,"feature2":1}]}'
    ```

=== "PowerShell"

    ```powershell
    $body = @{ instances = @(@{ feature1 = 1; feature2 = 1 }) } | ConvertTo-Json -Depth 3
    Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -ContentType application/json -Body $body
    ```

## Run with Docker

Build both targets and train into a shared named volume:

```bash
docker build --target train -t mlops-starter-kit:train .
docker build --target serve -t mlops-starter-kit:serve .
docker volume create model-artifacts
docker run --rm -v model-artifacts:/app/artifacts mlops-starter-kit:train
docker run --rm -p 127.0.0.1:8000:8000 -v model-artifacts:/app/artifacts:ro -e MODEL_PATH=/app/artifacts/models/baseline_model/v1.pkl mlops-starter-kit:serve
```

The runtime installs the package wheel and runs as a non-root user. The serving
container mounts artifacts read-only. Reuse the same dependency environment for
training and serving; cross-version pickle compatibility is not guaranteed.

## Deployment Boundary

Load only trusted artifacts. Before exposing the service beyond localhost, put
authentication and TLS in front of it and set request-size, timeout and rate
limits in a gateway. See [security](security.md) and the
[operable serving milestone](roadmap.md#m4-operable-serving).
