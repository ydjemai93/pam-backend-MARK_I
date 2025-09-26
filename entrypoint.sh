#!/bin/bash

# Railway entrypoint script
# Handles environment variable expansion for uvicorn

# Default port if Railway doesn't provide one
PORT=${PORT:-8000}

# Validate PORT is numeric
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "❌ Invalid PORT value: $PORT, using default 8000"
    PORT=8000
fi

echo "🚀 Starting FastAPI app on port $PORT"
echo "🔧 Current working directory: $(pwd)"
echo "🔧 Environment vars loaded: $(printenv | grep -E '^(SUPABASE|RAILWAY|PORT)' | wc -l)"

# Debug: Check if api/main.py exists
if [ -f "api/main.py" ]; then
    echo "✅ Found api/main.py"
else
    echo "❌ api/main.py not found! Contents:"
    ls -la
fi

# Start uvicorn with proper port
exec uvicorn api.main:app --host 0.0.0.0 --port $PORT
