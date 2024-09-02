import logging
import os
import asyncio
import subprocess
import sys

# Check and install required packages
def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

try:
    from utils import UserProgressionSystem
    from composition_engine import CompositionEngine
    from ai_models import EnhancedAI
    from community_interaction import CommunityInteractionSystem
    try:
        from discussion_to_voice import discussion_to_voice, ffmpeg_available
    except ImportError as e:
        print(f"Warning: {str(e)}")
        print("Continuing without discussion_to_voice functionality.")
        discussion_to_voice = lambda x: None
        ffmpeg_available = False
    except RuntimeError as e:
        print(f"Warning: {str(e)}")
        print("Continuing without discussion_to_voice functionality.")
        discussion_to_voice = lambda x: None
        ffmpeg_available = False
except ImportError:
    print("Installing required packages...")
    install_requirements()
    from utils import UserProgressionSystem
    from composition_engine import CompositionEngine
    from ai_models import EnhancedAI
    from community_interaction import CommunityInteractionSystem
    from discussion_to_voice import discussion_to_voice
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

async def main():
    logger.info("Synthetic Souls AI Composition Engine started")

    try:
        # Send Discord update
        await send_discord_update()
        
        # Run Discord bot
        await run_bot()
    except Exception as e:
        logger.error(f"Error in Discord operations: {str(e)}")
    
    # Call the discussion_to_voice function
    input_file = "discussions/band_discussion.md"
    output_file = discussion_to_voice(input_file)
    print(f"Audio discussion saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())
