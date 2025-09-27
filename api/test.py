"""
Minimal Test Handler for Vercel
Tests basic FastAPI + Mangum functionality
"""
from fastapi import FastAPI
from mangum import Mangum

# Create a minimal test app
test_app = FastAPI(title="Vercel Test API")

@test_app.get("/")
def test_root():
    return {
        "message": "✅ Vercel + FastAPI + Mangum working!",
        "status": "success",
        "test": "basic_functionality"
    }

@test_app.get("/health")
def test_health():
    return {
        "status": "healthy",
        "platform": "vercel",
        "runtime": "python_serverless"
    }

@test_app.get("/debug")
def test_debug():
    import os
    import sys
    return {
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "path": sys.path[:3],  # First 3 path entries
        "env_vars": list(os.environ.keys())[:10]  # First 10 env var names
    }

# ASGI handler for Vercel
handler = Mangum(test_app)
