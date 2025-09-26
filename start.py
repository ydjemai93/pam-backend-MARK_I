#!/usr/bin/env python3
"""
Railway startup script for FastAPI - NUCLEAR VERSION
Forces port 8000 and ignores Railway's broken $PORT
"""
import os
import subprocess
import sys

def main():
    # USE RAILWAY'S PORT (you're absolutely right!)
    port = os.environ.get('PORT', '8000')
    
    print(f"🚀 USING Railway PORT: {port}")
    print(f"🔥 NUCLEAR DB: Direct PostgreSQL (NO Supabase client)")
    print(f"🔧 Current working directory: {os.getcwd()}")
    print(f"🔧 ENV vars: SUPABASE_URL={os.environ.get('SUPABASE_URL', 'NOT_SET')[:50]}...")
    print(f"🔧 ENV vars: SERVICE_KEY={'SET' if os.environ.get('SUPABASE_SERVICE_ROLE_KEY') else 'NOT_SET'}")
    
    # Check if api/main.py exists
    if os.path.exists('api/main.py'):
        print("✅ Found api/main.py")
    else:
        print("❌ api/main.py not found! Contents:")
        print(os.listdir('.'))
    
    # Start uvicorn with Railway's PORT
    cmd = [
        'uvicorn', 
        'api.main:app', 
        '--host', '0.0.0.0', 
        '--port', port  # USE RAILWAY'S PORT!
    ]
    
    print(f"🚀 USING RAILWAY PORT: {' '.join(cmd)}")
    
    # Use exec to replace the current process
    os.execvp('uvicorn', cmd)

if __name__ == '__main__':
    main()
