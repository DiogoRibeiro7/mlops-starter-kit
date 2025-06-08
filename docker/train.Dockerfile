# Build stage: install ML libraries
FROM base AS builder

# Install ML-specific libraries
RUN pip install --no-cache-dir \
    torch torchvision \
    scikit-learn pandas numpy

# Final stage: copy only necessary artifacts
FROM base AS train

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Copy source code
COPY src/ /app/src/
WORKDIR /app

# Entry point for training
ENTRYPOINT ["python", "-m", "src.mlops_starter_kit.modeling.train"]
