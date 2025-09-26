# Optimized Dockerfile for Railway Deployment
# Handles Railway-specific requirements and dependency conflicts

FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# STABLE APPROACH: Use older working versions
RUN pip install --no-cache-dir six==1.16.0
RUN pip install --no-cache-dir python-dateutil==2.8.2
RUN pip install --no-cache-dir pytz==2022.7

# Copy and install requirements (supabase 1.0.3 - older stable version)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app

# Switch to non-root user
USER app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port (Railway will map to $PORT automatically)
EXPOSE 8000

# Alternative: Use inline script if entrypoint.sh fails
# CMD ["./entrypoint.sh"]
CMD ["sh", "-c", "PORT=${PORT:-8000}; echo \"🚀 Starting on port $PORT\"; exec uvicorn api.main:app --host 0.0.0.0 --port $PORT"]
