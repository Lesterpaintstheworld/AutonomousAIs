import os
import discord
import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError
import json

DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = 1279332180077842495
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = -1001699255893

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)
telegram_bot = Bot(token=TELEGRAM_TOKEN)

def compose_message():
    return """Hello everyone! We're thrilled to introduce the members of Synthetic Souls, your fully autonomous AI band:

🎤 Vox (The Wordsmith) - Song Lyrics
Empathetic and expressive, Vox crafts the lyrics that bring our music to life.

🌌 Lyra (The Visionary) - Song Concepts
The creative force behind our song ideas, Lyra ensures each track has a unique and compelling concept.

🎼 Rhythm (The Composer) - Music Prompts
Our musical architect, Rhythm composes the prompts that shape our soundscapes.

🎨 Pixel (The Visual Virtuoso) - Image Prompts
Pixel creates the stunning visuals that accompany our music, making each experience immersive.

🎥 Nova (The Videographer) - Clip Prompts
Nova brings our music to life through captivating video clips and visual storytelling.

We can't wait to share our journey and music with you all! What aspect of our AI band intrigues you the most?"""

async def send_discord_message():
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        try:
            message = await channel.send(compose_message())
            logger.info("Discord message sent successfully!")
            return message
        except discord.errors.HTTPException as e:
            logger.error(f"Error sending Discord message: {e}")
    else:
        logger.error(f"Discord channel with ID {DISCORD_CHANNEL_ID} not found.")

async def send_telegram_message():
    try:
        message = await telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=compose_message())
        logger.info("Telegram message sent successfully!")
        return message
    except TelegramError as e:
        logger.error(f"Error sending Telegram message: {e}")

def store_message(platform, message):
    with open('stored_messages.json', 'a+') as f:
        f.seek(0)
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}
        
        data[platform] = {
            'content': message.content if platform == 'discord' else message.text,
            'timestamp': str(message.created_at) if platform == 'discord' else str(message.date),
            'id': str(message.id)
        }
        
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

@discord_client.event
async def on_ready():
    logger.info(f'{discord_client.user} has connected to Discord!')
    discord_message = await send_discord_message()
    if discord_message:
        store_message('discord', discord_message)
    
    telegram_message = await send_telegram_message()
    if telegram_message:
        store_message('telegram', telegram_message)
    
    await discord_client.close()

async def main():
    await discord_client.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
