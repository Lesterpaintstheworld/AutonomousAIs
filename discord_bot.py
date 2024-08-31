import os
import discord
from discord.ext import commands

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
CHANNEL_ID = 1279332180077842495

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

async def send_discord_message(message):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(message)

def run_bot():
    bot.run(TOKEN)
