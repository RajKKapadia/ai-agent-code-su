"""Telegram webhook route"""
from fastapi import APIRouter, Request, Response, status
from typing import Dict, Any
import logging
import httpx
import os
from dotenv import load_dotenv

from agents import Runner
from src.agent import weather_agent

# Load environment variables
load_dotenv()

router = APIRouter()
logger = logging.getLogger(__name__)

async def send_telegram_message(chat_id: int, text: str) -> bool:
    """
    Send a message to a Telegram chat
    
    Args:
        chat_id: The chat ID to send the message to
        text: The message text to send
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent successfully to chat {chat_id}")
            return True
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {str(e)}")
        return False

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
        # Verify the secret token for security
        secret_token = os.getenv("TELEGRAM_SECRET_TOKEN")
        if secret_token:
            # Get the token from the request header
            request_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
            
            if request_token != secret_token:
                logger.warning("Invalid secret token received")
                return Response(
                    content={"ok": False, "error": "Unauthorized"},
                    status_code=status.HTTP_403_FORBIDDEN
                )
        
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
            
            # Process the message with AI Agent
            if text and chat_id:
                try:
                    # Run the agent with the user's message
                    result = await Runner.run(weather_agent, text)
                    
                    # Get the agent's response
                    agent_response = result.final_output
                    
                    logger.info(f"Agent response: {agent_response}")
                    
                    # Send the response back to Telegram
                    await send_telegram_message(chat_id, agent_response)
                    
                except Exception as agent_error:
                    logger.error(f"Error running agent: {str(agent_error)}")
                    # Send error message to user
                    await send_telegram_message(
                        chat_id, 
                        "Sorry, I encountered an error processing your message. Please try again."
                    )
            
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

