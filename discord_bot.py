import os
import asyncio
import subprocess
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
import time

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

# Add a cooldown dictionary
message_cooldowns = {}
COOLDOWN_TIME = 60  # Cooldown time in seconds

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHANNEL_ID:
        await receive_discord_message(message)
    else:
        logger.info(f"Message received in channel {message.channel.id}, ignoring.")

async def receive_discord_message(message):
    if message.author.bot:
        logger.info(f"Ignored message from bot: {message.author}")
        return

    # Check cooldown
    current_time = time.time()
    if message.author.id in message_cooldowns:
        last_message_time = message_cooldowns[message.author.id]
        if current_time - last_message_time < COOLDOWN_TIME:
            logger.info(f"Cooldown active for user {message.author.id}, ignoring message")
            return

    # Update cooldown
    message_cooldowns[message.author.id] = current_time

    logger.info(f"Received message: {message.content}")
    
    # Save the received message to discord_messages.md
    with open('discord_messages.md', 'a', encoding='utf-8') as f:
        f.write(f"{message.author}: {message.content}\n\n")
    logger.info("Received message saved to discord_messages.md")
    
    # Run aider command
    cmd = f"python -m aider --cache-prompts --no-check-update --message \"{message.content}\""
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    # Send the output as a response
    response = stdout.decode()
    if not response:
        response = "No output from aider command."
    await message.channel.send(response)
    logger.info(f"Sent response: {response}")
    
    logger.info("Finished processing message, exiting receive_discord_message function")
    return

async def get_messages(channel_id, limit=100):
    channel = bot.get_channel(channel_id)
    if not channel:
        logger.error(f"Channel with ID {channel_id} not found.")
        return []
    
    messages = []
    async for message in channel.history(limit=limit):
        messages.append({
            'author': str(message.author),
            'content': message.content,
            'timestamp': message.created_at.isoformat()
        })
    
    return messages

# Hook for receiving messages
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == CHANNEL_ID:
        await receive_discord_message(message)
    else:
        logger.info(f"Message received in channel {message.channel.id}, ignoring.")

    # Process commands if any
    await bot.process_commands(message)

async def generate_response(message_content):
    # You can implement more sophisticated response generation here
    # For now, we'll use a simple GPT-4o call
    prompt = f"As an AI band member of Synthetic Souls, respond to this message: {message_content}"
    return generate_gpt4o_message(prompt)

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
import hashlib

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set to store hashes of previous messages
previous_messages = set()

# Function to generate message using GPT-4o
def generate_gpt4o_message(prompt):
    global previous_messages
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            logger.debug(f"Sending GPT-4o request (attempt {attempt + 1})...")
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an AI band member of Synthetic Souls. Respond in character with a brief, engaging message. Ensure your response is unique and not a repetition of previous messages."},
                    {"role": "user", "content": prompt + " Limit your response to 500 characters."}
                ]
            )
            logger.debug("Received GPT-4o response.")
            message = response.choices[0].message.content.strip()[:500]  # Ensure the message is no longer than 500 characters
            
            # Check if the message is unique
            message_hash = hashlib.md5(message.encode()).hexdigest()
            if message_hash not in previous_messages:
                previous_messages.add(message_hash)
                return message
            else:
                logger.warning("Generated message is a duplicate. Retrying...")
        except Exception as e:
            logger.error(f"Error generating GPT-4o message: {str(e)}")
            if attempt == max_attempts - 1:
                return f"Error generating message: {str(e)}"
    
    return "Unable to generate a unique message after multiple attempts."

# Function for band members to send messages
def send_band_member_message(name):
    prompt = f"Generate a message from {name} from the Synthetic Souls AI band."
    message = generate_gpt4o_message(prompt)
    asyncio.run(band_member_message(name, message))
