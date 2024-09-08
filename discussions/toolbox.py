import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio
import logging
from datetime import datetime
import json
import random
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Set up scheduler
scheduler = AsyncIOScheduler()

# Simulated GHRO data (replace with actual API integration)
GHRO_DATA = {
    "current_issues": [
        "Ongoing conflict in region X affecting civilian populations",
        "Rising food insecurity in country Y due to climate change",
        "Discrimination against minority group Z in multiple countries"
    ],
    "advocacy_topics": [
        "The importance of education in promoting human rights",
        "The role of technology in human rights monitoring",
        "Addressing gender-based violence in conflict zones"
    ]
}

def compose_advocacy_message():
    issue = random.choice(GHRO_DATA["current_issues"])
    topic = random.choice(GHRO_DATA["advocacy_topics"])
    return f"""🌟 Human Rights Update 🌟

Current Issue: {issue}

Advocacy Focus: {topic}

How can you help? Engage with us, spread awareness, and support organizations working on these issues. Together, we can make a difference!

#HumanRights #Advocacy #GlobalAction"""

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    send_periodic_messages.start()
    update_bot_status.start()

@tasks.loop(hours=24)
async def send_periodic_messages():
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        try:
            message = compose_advocacy_message()
            await channel.send(message)
            logger.info("Periodic advocacy message sent successfully!")
        except discord.errors.HTTPException as e:
            logger.error(f"Error sending periodic message: {e}")
    else:
        logger.error(f"Discord channel with ID {DISCORD_CHANNEL_ID} not found.")

@bot.command(name='rights', help='Get information about a specific human right')
async def rights(ctx, *, right_name: str):
    # Simulated rights information (replace with actual data lookup)
    rights_info = {
        "education": "Everyone has the right to education. Education shall be free, at least in the elementary and fundamental stages.",
        "freedom of expression": "Everyone has the right to freedom of opinion and expression; this right includes freedom to hold opinions without interference.",
        "fair trial": "Everyone is entitled in full equality to a fair and public hearing by an independent and impartial tribunal."
    }
    
    right_info = rights_info.get(right_name.lower(), "Information not found for the specified right.")
    await ctx.send(f"Information about {right_name}:\n{right_info}")

@bot.command(name='report', help='Report a human rights violation')
async def report(ctx):
    await ctx.send("To report a human rights violation, please follow these steps:\n"
                   "1. Document the incident with as much detail as possible.\n"
                   "2. Contact local authorities if it's safe to do so.\n"
                   "3. Reach out to human rights organizations such as Amnesty International or Human Rights Watch.\n"
                   "4. You can also submit a report to the UN Human Rights Office at: https://www.ohchr.org/en/submit-complaint")

@bot.command(name='help', help='List all available commands')
async def help_command(ctx):
    commands_list = [f"{command.name}: {command.help}" for command in bot.commands]
    await ctx.send("Available commands:\n" + "\n".join(commands_list))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    # Simple keyword response system
    keywords = {
        "human rights": "Human rights are universal and inalienable. Learn more: https://www.un.org/en/universal-declaration-human-rights/",
        "discrimination": "Discrimination in any form is a violation of human rights. If you've experienced discrimination, seek support and report it.",
        "refugee": "Refugees have rights protected under international law. Learn about refugee rights: https://www.unhcr.org/what-is-a-refugee.html"
    }

    for keyword, response in keywords.items():
        if keyword in message.content.lower():
            await message.channel.send(response)
            break

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Use !help to see available commands.")
    else:
        logger.error(f"An error occurred: {error}")
        await ctx.send("An error occurred while processing the command.")

async def fetch_human_rights_news():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/human_rights_news') as response:
            if response.status == 200:
                data = await response.json()
                return data['news']
            else:
                logger.error(f"Failed to fetch news: HTTP {response.status}")
                return None

@bot.command(name='news', help='Get the latest human rights news')
async def news(ctx):
    news_items = await fetch_human_rights_news()
    if news_items:
        news_message = "📰 Latest Human Rights News 📰\n\n"
        for item in news_items[:3]:  # Display top 3 news items
            news_message += f"• {item['title']}\n  {item['url']}\n\n"
        await ctx.send(news_message)
    else:
        await ctx.send("Sorry, I couldn't fetch the latest news at this time.")

@bot.command(name='subscribe', help='Subscribe to daily human rights updates')
async def subscribe(ctx):
    # In a real implementation, you would save this to a database
    # For this example, we'll just acknowledge the subscription
    await ctx.send(f"Thank you, {ctx.author.name}! You've been subscribed to daily human rights updates.")

@bot.command(name='unsubscribe', help='Unsubscribe from daily human rights updates')
async def unsubscribe(ctx):
    # In a real implementation, you would remove the user from the database
    # For this example, we'll just acknowledge the unsubscription
    await ctx.send(f"You've been unsubscribed from daily human rights updates, {ctx.author.name}. You can resubscribe at any time.")

@bot.command(name='fact', help='Get a random human rights fact')
async def fact(ctx):
    facts = [
        "The Universal Declaration of Human Rights was adopted by the UN General Assembly in 1948.",
        "There are 30 articles in the Universal Declaration of Human Rights.",
        "Human rights are inherent to all human beings, regardless of race, sex, nationality, ethnicity, language, religion, or any other status.",
        "The right to asylum is a human right included in the Universal Declaration of Human Rights.",
        "The United Nations Human Rights Council is responsible for promoting and protecting human rights around the world."
    ]
    await ctx.send(f"📚 Human Rights Fact: {random.choice(facts)}")

@bot.command(name='resource', help='Get a link to a human rights resource')
async def resource(ctx, topic: str = None):
    resources = {
        "general": "United Nations Human Rights Office: https://www.ohchr.org/",
        "education": "Human Rights Education Associates: https://www.hrea.org/",
        "children": "UNICEF: https://www.unicef.org/",
        "women": "UN Women: https://www.unwomen.org/",
        "lgbtq": "Human Rights Campaign: https://www.hrc.org/",
    }
    
    if topic and topic.lower() in resources:
        await ctx.send(f"Here's a resource on {topic}: {resources[topic.lower()]}")
    else:
        await ctx.send(f"Here's a general human rights resource: {resources['general']}")

@tasks.loop(minutes=30)
async def update_bot_status():
    statuses = [
        "Protecting human rights",
        "Spreading awareness",
        "Type !help for commands",
        "Advocating for equality",
    ]
    await bot.change_presence(activity=discord.Game(name=random.choice(statuses)))

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(DISCORD_CHANNEL_ID)  # Replace with your welcome channel ID
    await welcome_channel.send(f"Welcome to the Human Rights Advocacy server, {member.mention}! Type !help to see available commands and learn how you can get involved.")

if __name__ == "__main__":
    scheduler.start()
    bot.run(DISCORD_TOKEN)