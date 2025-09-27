"""
Vercel Handler for FastAPI - Debug Version
Provides ASGI adapter with absolute imports
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from mangum import Mangum
    print("✅ Mangum imported successfully")
    
    # Try absolute import instead of relative
    import main
    app = main.app
    print("✅ FastAPI app imported successfully")
    
    # ASGI adapter for Vercel serverless
    handler = Mangum(app)
    print("✅ Mangum handler created successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Create a minimal FastAPI app as fallback
    from fastapi import FastAPI
    fallback_app = FastAPI()
    
    @fallback_app.get("/")
    def fallback_root():
        return {"error": f"Import failed: {str(e)}", "status": "fallback_mode"}
    
    @fallback_app.get("/health")
    def fallback_health():
        return {"status": "fallback_working", "error": f"Main app import failed: {str(e)}"}
    
    handler = Mangum(fallback_app)

except Exception as e:
    print(f"❌ Other error: {e}")
    from fastapi import FastAPI
    error_app = FastAPI()
    
    @error_app.get("/")
    def error_root():
        return {"error": f"General error: {str(e)}", "status": "error_mode"}
    
    handler = Mangum(error_app)
