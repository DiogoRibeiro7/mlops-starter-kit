# Inherit from base image
FROM mlops-starter-kit-base:latest

# Install ML-specific libs (e.g., torch, scikit-learn)
RUN pip install --no-cache-dir \
    torch torchvision \
    scikit-learn pandas numpy

# Copy source code
COPY src/ /app/src/
WORKDIR /app

# Entry point for training
ENTRYPOINT ["python", "-m", "src.mlops_starter_kit.modeling.train"]
