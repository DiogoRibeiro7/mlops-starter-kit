# Build stage: install serving dependencies
FROM python:3.10-slim AS builder
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Final stage: lightweight runtime
FROM python:3.10-slim AS serve
WORKDIR /app

# Copy only Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Copy application code
COPY src/ /app/src/

# Expose serving port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "src.mlops_starter_kit.api:app", "--host", "0.0.0.0", "--port", "8000"]
