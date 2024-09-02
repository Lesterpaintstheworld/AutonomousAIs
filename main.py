import logging
import os
import asyncio
import subprocess
import sys

# Check and install required packages
def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

try:
    from discussion_to_voice import discussion_to_voice, check_ffmpeg
except ImportError:
    print("Installing required packages...")
    install_requirements()
    from discussion_to_voice import discussion_to_voice, check_ffmpeg
try:
    from discord_bot import send_discord_message, run_bot, send_band_member_message
except ImportError:
    print("Error: discord module not found. Please ensure it's installed correctly.")
    print("Try running: pip install -U discord.py")
    send_discord_message = run_bot = send_band_member_message = lambda *args, **kwargs: None
import random
import asyncio
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of band members
band_members = ["Lyra", "Vox", "Rhythm", "Nova"]

async def send_discord_update():
    try:
        # Choose a random band member to send the startup message
        random_member = random.choice(band_members)
        await send_band_member_message(random_member)
    except Exception as e:
        logger.error(f"Failed to send Discord update: {str(e)}")

def main():
    logger.info("Synthetic Souls AI Composition Engine started")

    try:
        # Send Discord update
        asyncio.get_event_loop().run_until_complete(send_discord_update())
        
        # Run discussion_to_voice
        check_ffmpeg()
        input_file = "discussions/band_discussion.md"
        output_file = discussion_to_voice(input_file)
        print(f"Audio discussion saved as: {output_file}")
        
        # Run Discord bot
        run_bot()
    except Exception as e:
        logger.error(f"Error in operations: {str(e)}")
