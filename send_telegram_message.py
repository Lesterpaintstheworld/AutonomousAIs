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

# Send Vox's introduction post
with open('posts/vox_introduction_post.md', 'r', encoding='utf-8') as file:
    vox_intro = file.read()

# Split the message into chunks of 4096 characters or less
max_length = 4096
message_chunks = [vox_intro[i:i+max_length] for i in range(0, len(vox_intro), max_length)]

# Send each chunk as a separate message
for chunk in message_chunks:
    send_telegram_message(chunk)

# Test command
if __name__ == "__main__":
    test_message = "This is a test message from the Synthetic Souls project!"
    success = send_telegram_message(test_message)
    print(f"Test message sent successfully: {success}")
