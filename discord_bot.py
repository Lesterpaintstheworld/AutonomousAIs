import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = 1279332180077842495

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set")

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
