import os
import requests
import sys
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_telegram_message.py <message>")
        sys.exit(1)
    
    message = ' '.join(sys.argv[1:])
    
    # Split the message into chunks of 4096 characters or less
    max_length = 4096
    message_chunks = [message[i:i+max_length] for i in range(0, len(message), max_length)]
    
    # Send each chunk as a separate message
    for chunk in message_chunks:
        success = send_telegram_message(chunk)
        print(f"Message chunk sent successfully: {success}")
