"""Telegram webhook route"""
from fastapi import APIRouter, Request, Response, status
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook", status_code=status.HTTP_200_OK)
async def telegram_webhook(request: Request):
    """
    Telegram webhook endpoint to receive updates from Telegram server
    
    Args:
        request: The incoming request from Telegram
        
    Returns:
        dict: Acknowledgment response
    """
    try:
        # Get the JSON payload from Telegram
        update: Dict[Any, Any] = await request.json()
        
        # Log the received update
        logger.info(f"Received Telegram update: {update}")
        
        # Extract message information if available
        if "message" in update:
            message = update["message"]
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            user = message.get("from", {})
            
            logger.info(f"Message from {user.get('username', 'unknown')}: {text}")
            
            # TODO: Process the message with AI Agent
            # This is where you'll integrate your AI agent logic
            
        # Telegram expects a 200 OK response
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Error processing Telegram webhook: {str(e)}")
        return Response(
            content={"ok": False, "error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/info")
async def telegram_info():
    """
    Get information about the Telegram webhook endpoint
    
    Returns:
        dict: Webhook endpoint information
    """
    return {
        "webhook_endpoint": "/telegram/webhook",
        "method": "POST",
        "description": "Endpoint to receive updates from Telegram server"
    }

