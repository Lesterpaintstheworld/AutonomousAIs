import os
from dotenv import load_dotenv
import discord
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
    bot.run(TOKEN)

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

# Function to generate message using GPT-4
def generate_gpt4_message(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI band member of Synthetic Souls. Respond in character."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating GPT-4 message: {str(e)}")
        return f"Error generating message: {str(e)}"

# Function for band members to send messages
def send_band_member_message(name):
    prompt = f"Generate a message for {name} from Synthetic Souls"
    message = generate_gpt4_message(prompt)
    asyncio.run(band_member_message(name, message))
