# Use a lightweight ASGI server base
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install minimal serving deps
COPY requirements.txt ./
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy application code
COPY src/ /app/src/

# Expose serving port
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "src.mlops_starter_kit.api:app", "--host", "0.0.0.0", "--port", "8000"]
