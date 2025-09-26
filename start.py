#!/usr/bin/env python3
"""
Railway startup script for FastAPI - NUCLEAR VERSION
Forces port 8000 and ignores Railway's broken $PORT
"""
import os
import subprocess
import sys

def main():
    # NUCLEAR APPROACH: IGNORE Railway's PORT entirely
    port = '8000'
    
    # Debug: Show what Railway is actually providing
    railway_port = os.environ.get('PORT', 'NOT_SET')
    print(f"🔥 NUCLEAR MODE: Ignoring Railway PORT={railway_port}")
    print(f"🔥 FORCED PORT: {port}")
    print(f"🔧 Current working directory: {os.getcwd()}")
    print(f"🔧 All ENV vars: {list(os.environ.keys())}")
    
    # Check if api/main.py exists
    if os.path.exists('api/main.py'):
        print("✅ Found api/main.py")
    else:
        print("❌ api/main.py not found! Contents:")
        print(os.listdir('.'))
    
    # Start uvicorn with FORCED port 8000
    cmd = [
        'uvicorn', 
        'api.main:app', 
        '--host', '0.0.0.0', 
        '--port', '8000'  # HARD-CODED NO VARIABLES
    ]
    
    print(f"🚀 NUCLEAR COMMAND: {' '.join(cmd)}")
    
    # Use exec to replace the current process
    os.execvp('uvicorn', cmd)

if __name__ == '__main__':
    main()
