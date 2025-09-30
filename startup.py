#!/usr/bin/env python3
"""
Azure Web App startup script for PAM Backend API
This script ensures the FastAPI app starts correctly in Azure Web App environment
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (Azure sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    # Start the FastAPI app
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=port,
        workers=1
    )
