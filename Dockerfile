# Clean Dockerfile for Railway Deployment - FORCE REBUILD 2025-01-10 16:15
# Fixed supabase installation and removed all nuclear code

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

# FIX FOR SIX.MOVES._THREAD ERROR - WORKING VERSIONS
RUN pip install --no-cache-dir six==1.16.0
RUN pip install --no-cache-dir python-dateutil==2.9.0
RUN pip install --no-cache-dir pytz==2023.3

# FORCE CACHE INVALIDATION - BUILD 2025-01-10-16:15
RUN echo "Clean build - no cache"

# Copy and install requirements with working versions
COPY requirements.fixed.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Verify supabase is installed
RUN python -c "import supabase; print('✅ Supabase installed:', supabase.__version__)"
RUN pip list | grep -E "(supabase|six|dateutil)"

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

# Railway handles port mapping automatically  
EXPOSE 8000

# Simple CMD that works - Railway provides $PORT
CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT
