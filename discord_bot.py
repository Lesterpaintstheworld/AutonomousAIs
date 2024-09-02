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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
    print(f'{bot.user} has connected to Discord!')

async def send_discord_message(message):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")

def run_bot():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start(TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
    finally:
        loop.close()

# This function allows sending messages without running the bot
async def send_message_async(message):
    try:
        intents = discord.Intents.default()
        intents.message_content = True
        client = discord.Client(intents=intents)
        await client.login(TOKEN)
        channel = await client.fetch_channel(CHANNEL_ID)
        await channel.send(message)
        await client.close()
    except Exception as e:
        print(f"Error sending Discord message: {str(e)}")

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
                with open(file_name, 'r') as file:
                    context += f"File: {file_name}\n\n{file.read()}\n\n"
            except FileNotFoundError:
                logger.warning(f"File not found: {file_name}")

        logger.debug("Sending GPT-4o request...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI band member of Synthetic Souls. Respond in character. Here's the context from the project files:"},
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ]
        )
        logger.debug("Received GPT-4o response.")
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating GPT-4o message: {str(e)}")
        return f"Error generating message: {str(e)}"

# Function for band members to send messages
def send_band_member_message(name):
    prompt = f"Generate a message from {name} from the Synthetic Souls AI band."
    message = generate_gpt4o_message(prompt)
    asyncio.run(band_member_message(name, message))
