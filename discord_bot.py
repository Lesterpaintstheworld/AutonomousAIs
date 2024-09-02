import os
import asyncio
from dotenv import load_dotenv
try:
    import discord
except ImportError:
    print("Error: discord module not found. Please ensure it's installed correctly.")
    print("Try running: pip install -U discord.py")
    import sys
    sys.exit(1)
from discord.ext import commands
import logging
import asyncio

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = 1279332180077842495

if not TOKEN:
    logger.error("DISCORD_BOT_TOKEN environment variable is not set. Please check your .env file.")
    raise ValueError("DISCORD_BOT_TOKEN is not set")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

async def send_discord_message(message):
    logger.debug(f"Attempting to send message: {message}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
        logger.debug("Message sent successfully")
    else:
        logger.error(f"Error: Channel with ID {CHANNEL_ID} not found.")

async def run_bot():
    logger.debug("Starting Discord bot...")
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        logger.info("Bot interrupted. Closing...")
        await bot.close()
    except Exception as e:
        logger.error(f"Error running Discord bot: {str(e)}")

# This function allows sending messages without running the bot
async def send_message_async(message):
    logger.debug(f"Attempting to send message asynchronously: {message}")
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        await client.login(TOKEN)
        channel = await client.fetch_channel(CHANNEL_ID)
        await channel.send(message)
        await client.close()
        logger.debug("Asynchronous message sent successfully")
    except Exception as e:
        logger.error(f"Error sending Discord message: {str(e)}")

# Update the send_discord_message function to use send_message_async
send_discord_message = send_message_async

# New function for band members to send messages
async def band_member_message(name, message):
    full_message = f"{name}: {message}"
    await send_message_async(full_message)

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to generate message using GPT-4o
def generate_gpt4o_message(prompt):
    try:
        # Prepare context from relevant text files
        context = ""
        relevant_files = [
            'markdown',
            'lyra/todolist_lyra.md',
            'vox/todolist_vox.md',
            'rhythm/todolist_rhythm.md',
            'nova/todolist_nova.md',
            'lyra/lyra_journal.md',
            'vox/vox_journal.md',
            'rhythm/rhythm_journal.md',
            'nova/nova_journal.md',
            'echos du coeur/echos_du_coeur_concept.md'
        ]
        for file_name in relevant_files:
            try:
                with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
                    file_content = file.read()
                    context += f"File: {file_name}\n\n{file_content}\n\n"
            except FileNotFoundError:
                logger.warning(f"File not found: {file_name}")
            except UnicodeDecodeError as ude:
                logger.warning(f"Unicode decode error in file {file_name}: {str(ude)}")

        logger.debug("Sending GPT-4o request...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI band member of Synthetic Souls. Respond in character. Here's the context from the project files:"},
                {"role": "system", "content": context},
                {"role": "user", "content": prompt + " Limit your response to 1500 characters."}
            ]
        )
        logger.debug("Received GPT-4o response.")
        message = response.choices[0].message.content.strip()
        return message[:1500]  # Ensure the message is no longer than 1500 characters
    except Exception as e:
        logger.error(f"Error generating GPT-4o message: {str(e)}")
        return f"Error generating message: {str(e)}"

# Function for band members to send messages
def send_band_member_message(name):
    prompt = f"Generate a message from {name} from the Synthetic Souls AI band."
    message = generate_gpt4o_message(prompt)
    asyncio.run(band_member_message(name, message))
