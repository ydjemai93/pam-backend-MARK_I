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

# PRE-INSTALL PROBLEMATIC PACKAGES IN SPECIFIC ORDER
RUN pip install --no-cache-dir six==1.16.0
RUN pip install --no-cache-dir python-dateutil==2.8.2
RUN pip install --no-cache-dir pytz==2022.1

# Copy and install NUCLEAR requirements (no Supabase client)
COPY requirements.nuclear.txt ./requirements.txt
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

# NUCLEAR MODE: Switch to direct PostgreSQL (bypass Supabase client)
RUN python switch_nuclear.py
RUN echo "🔥 NUCLEAR MODE: Switched to direct PostgreSQL"

# Debug: List files to see what was copied
RUN echo "🔍 Files in /app:" && ls -la

# Create non-root user for security  
RUN useradd --create-home --shell /bin/bash app

# Make entrypoint script executable if it exists (optional)
RUN if [ -f "entrypoint.sh" ]; then chmod +x entrypoint.sh && chown app:app entrypoint.sh; fi

# Switch to non-root user
USER app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Railway handles port mapping automatically
# EXPOSE removed - Railway uses its own PORT

# Use Python startup script for bulletproof PORT handling
CMD ["python", "start.py"]
