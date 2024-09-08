import discord
from discord.ext import commands
import asyncio
from discord_bot import generate_gpt4o_message, CHANNEL_ID, TOKEN

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await send_introduction(channel)
    else:
        print(f"Error: Channel with ID {CHANNEL_ID} not found.")
    await bot.close()

async def send_introduction(channel):
    intro_prompt = "Generate a brief, engaging introduction for an AI band member of Synthetic Souls joining a Discord server. Include a greeting, your role, and an invitation for interaction."
    intro_message = generate_gpt4o_message(intro_prompt)
    await channel.send(intro_message)

async def main():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Error running Discord bot: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
