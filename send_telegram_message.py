import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_telegram_message(message):
    """
    Send a message to the specified Telegram channel.
    
    Args:
    message (str): The message to be sent.
    
    Returns:
    bool: True if the message was sent successfully, False otherwise.
    """
    token = os.getenv('TELEGRAM_API_TOKEN')
    channel_id = "-1001699255893"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": message
    }
    
    response = requests.post(url, data=data)
    
    return response.status_code == 200

# Example usage:
# send_telegram_message("Hello, this is a test message from the Synthetic Souls project!")
