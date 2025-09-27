"""
Vercel Handler for FastAPI
Provides ASGI adapter without modifying main.py
"""
from mangum import Mangum
from .main import app

# ASGI adapter for Vercel serverless
handler = Mangum(app)
