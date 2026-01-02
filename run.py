"""Run the FastAPI application"""
import uvicorn
from dotenv import load_dotenv
import os

def main():
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables or use defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    # Run the FastAPI application
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload
    )

if __name__ == "__main__":
    main()
