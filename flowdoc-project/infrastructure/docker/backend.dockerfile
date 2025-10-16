FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/app ./app
COPY backend/config ./config

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=production

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]