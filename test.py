"""Script to set and manage Telegram webhook"""
import httpx
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()


async def set_telegram_webhook(webhook_url: str = None) -> dict:
    """
    Set the Telegram webhook with secret token
    
    Args:
        webhook_url: The webhook URL (optional, will use default if not provided)
        
    Returns:
        dict: Response from Telegram API
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    secret_token = os.getenv("TELEGRAM_SECRET_TOKEN")
    
    if not bot_token:
        return {"ok": False, "error": "TELEGRAM_BOT_TOKEN not found in .env file"}
    
    if not secret_token:
        return {"ok": False, "error": "TELEGRAM_SECRET_TOKEN not found in .env file"}
    
    # Use provided webhook_url or get from environment
    if not webhook_url:
        webhook_url = os.getenv("TELEGRAM_WEBHOOK_URL")
    
    if not webhook_url:
        return {"ok": False, "error": "webhook_url not provided and TELEGRAM_WEBHOOK_URL not found in .env file"}
    
    # Telegram API endpoint
    url = f"https://api.telegram.org/bot{bot_token}/setWebhook"
    
    # Payload with webhook URL and secret token
    payload = {
        "url": webhook_url,
        "secret_token": secret_token,
        "drop_pending_updates": True  # Optional: drop any pending updates
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            result = response.json()
            return result
    except httpx.HTTPStatusError as e:
        return {"ok": False, "error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# async def get_webhook_info() -> dict:
#     """
#     Get current webhook information
    
#     Returns:
#         dict: Current webhook status from Telegram API
#     """
#     bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
#     if not bot_token:
#         return {"ok": False, "error": "TELEGRAM_BOT_TOKEN not found in .env file"}
    
#     url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, timeout=10.0)
#             response.raise_for_status()
#             result = response.json()
#             return result
#     except Exception as e:
#         return {"ok": False, "error": str(e)}


# async def delete_webhook() -> dict:
#     """
#     Delete the current webhook
    
#     Returns:
#         dict: Response from Telegram API
#     """
#     bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
#     if not bot_token:
#         return {"ok": False, "error": "TELEGRAM_BOT_TOKEN not found in .env file"}
    
#     url = f"https://api.telegram.org/bot{bot_token}/deleteWebhook"
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, timeout=10.0)
#             response.raise_for_status()
#             result = response.json()
#             return result
#     except Exception as e:
#         return {"ok": False, "error": str(e)}


# async def main():
#     """Main function to demonstrate webhook management"""
#     import sys
    
#     if len(sys.argv) < 2:
#         print("Usage:")
#         print("  python test.py set <webhook_url>     - Set webhook")
#         print("  python test.py set                   - Set webhook from .env")
#         print("  python test.py info                  - Get webhook info")
#         print("  python test.py delete                - Delete webhook")
#         return
    
#     command = sys.argv[1].lower()
    
#     if command == "set":
#         webhook_url = sys.argv[2] if len(sys.argv) > 2 else None
#         print("Setting webhook...")
#         result = await set_telegram_webhook(webhook_url)
        
#         if result.get("ok"):
#             print("✅ Webhook set successfully!")
#             print(f"Response: {result}")
            
#             # Get webhook info to confirm
#             print("\nCurrent webhook info:")
#             info = await get_webhook_info()
#             if info.get("ok"):
#                 webhook_result = info.get("result", {})
#                 print(f"  URL: {webhook_result.get('url')}")
#                 print(f"  Pending updates: {webhook_result.get('pending_update_count', 0)}")
#         else:
#             print(f"❌ Failed to set webhook: {result.get('error')}")
#             if "details" in result:
#                 print(f"Details: {result['details']}")
    
#     elif command == "info":
#         print("Getting webhook info...")
#         result = await get_webhook_info()
        
#         if result.get("ok"):
#             webhook_info = result.get("result", {})
#             print("\n📊 Webhook Information:")
#             print(f"  URL: {webhook_info.get('url', 'Not set')}")
#             print(f"  Has custom certificate: {webhook_info.get('has_custom_certificate', False)}")
#             print(f"  Pending updates: {webhook_info.get('pending_update_count', 0)}")
#             print(f"  Max connections: {webhook_info.get('max_connections', 'N/A')}")
            
#             if webhook_info.get('last_error_date'):
#                 print(f"  ⚠️ Last error: {webhook_info.get('last_error_message')}")
#                 print(f"  Last error date: {webhook_info.get('last_error_date')}")
#         else:
#             print(f"❌ Failed to get webhook info: {result.get('error')}")
    
#     elif command == "delete":
#         print("Deleting webhook...")
#         result = await delete_webhook()
        
#         if result.get("ok"):
#             print("✅ Webhook deleted successfully!")
#         else:
#             print(f"❌ Failed to delete webhook: {result.get('error')}")
    
#     else:
#         print(f"Unknown command: {command}")
#         print("Use: set, info, or delete")


# if __name__ == "__main__":
#     asyncio.run(main())


asyncio.run(set_telegram_webhook(
    webhook_url="https://e889806ef23a.ngrok-free.app/telegram/webhook"
))
