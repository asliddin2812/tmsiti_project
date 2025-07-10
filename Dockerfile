# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_BUILD_ISOLATION=1 \
    PIP_ONLY_BINARY=:all:

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install pydantic via binary only
RUN pip install --only-binary pydantic,pydantic-core \
    pydantic==2.5.0 \
    pydantic-settings==2.1.0

# Copy requirements and install remaining dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create folders for media/static
RUN mkdir -p static/uploads static/default

# Create a non-root user
RUN useradd --create-home --shell /bin/bash tmsiti \
    && chown -R tmsiti:tmsiti /app

USER tmsiti

# Expose FastAPI port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
