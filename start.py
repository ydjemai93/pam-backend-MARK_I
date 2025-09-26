#!/usr/bin/env python3
"""
Railway startup script for FastAPI
Handles PORT environment variable properly
"""
import os
import subprocess
import sys

def main():
    # Get PORT from environment, default to 8000
    port = os.environ.get('PORT', '8000')
    
    # Validate port is numeric
    try:
        port_int = int(port)
        if port_int < 1 or port_int > 65535:
            raise ValueError("Port out of range")
    except ValueError:
        print(f"❌ Invalid PORT value: {port}, using default 8000")
        port = '8000'
    
    print(f"🚀 Starting FastAPI app on port {port}")
    print(f"🔧 Current working directory: {os.getcwd()}")
    print(f"🔧 Environment variables loaded: {len([k for k in os.environ.keys() if k.startswith(('SUPABASE', 'RAILWAY', 'PORT'))])}")
    
    # Check if api/main.py exists
    if os.path.exists('api/main.py'):
        print("✅ Found api/main.py")
    else:
        print("❌ api/main.py not found! Contents:")
        print(os.listdir('.'))
    
    # Start uvicorn
    cmd = [
        'uvicorn', 
        'api.main:app', 
        '--host', '0.0.0.0', 
        '--port', port
    ]
    
    print(f"🚀 Executing: {' '.join(cmd)}")
    
    # Use exec to replace the current process
    os.execvp('uvicorn', cmd)

if __name__ == '__main__':
    main()
