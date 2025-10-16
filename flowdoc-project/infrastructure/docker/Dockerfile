# Flowdoc Application Dockerfile
# Multi-stage build for smaller final image
FROM python:3.11-slim-bullseye as builder

WORKDIR /app

# Set Flowdoc version
ARG FLOWDOC_VERSION=2.0.0
ENV FLOWDOC_VERSION=${FLOWDOC_VERSION}

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim-bullseye

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install Python packages
RUN pip install --no-cache /wheels/*

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=src
ENV FLASK_ENV=production
ENV WORKERS=4

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run gunicorn
CMD gunicorn -w ${WORKERS} -b 0.0.0.0:8000 "src:create_app()"