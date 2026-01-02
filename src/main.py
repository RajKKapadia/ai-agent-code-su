"""Main FastAPI application"""
from fastapi import FastAPI
from src.routes import health, telegram

app = FastAPI(
    title="AI Agent Code SU",
    description="Telegram Bot with AI Agent",
    version="0.1.0"
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(telegram.router, prefix="/telegram", tags=["Telegram"])

@app.get("/")
async def root():
    return {
        "message": "AI Agent Code SU API",
        "status": "running"
    }

