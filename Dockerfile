# Azure-Optimized Dockerfile
FROM python:3.12-slim

# Install system dependencies for Linux
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements-azure.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Azure Container Apps expects port 80 by default
EXPOSE 80

# Start command (Azure will inject PORT=80)
CMD ["sh", "-c", "PORT=${PORT:-80}; uvicorn api.main:app --host 0.0.0.0 --port $PORT"]