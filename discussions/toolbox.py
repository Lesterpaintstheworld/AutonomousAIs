import os
import asyncio
import logging
import click
import discord
from discord.ext import commands
from telegram import Bot as TelegramBot
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite3
import json
from datetime import datetime, timedelta
import random  # Importing the random module

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load tokens from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
discord_bot = commands.Bot(command_prefix='!', intents=intents)

# Set up Telegram bot
telegram_bot = TelegramBot(token=TELEGRAM_TOKEN)

# Set up scheduler
scheduler = AsyncIOScheduler()

# Database setup
conn = sqlite3.connect('messages.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY, platform TEXT, target TEXT, content TEXT, scheduled_time TEXT)''')
conn.commit()

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

@click.group()
def cli():
    """CLI for managing Discord and Telegram bots."""
    pass

@cli.command()
@click.option('--platform', type=click.Choice(['discord', 'telegram']), required=True, help='Choose the platform to send the message')
@click.option('--target', required=True, help='Channel/chat ID or name to send the message to')
@click.option('--message', required=True, help='Content of the message')
@click.option('--schedule', type=click.DateTime(), help='Schedule the message for a future time (format: YYYY-MM-DD HH:MM:SS)')
def send(platform, target, message, schedule):
    """Send a message to the specified platform and target."""
    if schedule:
        scheduler.add_job(send_message, 'date', run_date=schedule, args=[platform, target, message])
        click.echo(f"Message scheduled for {schedule}")
    else:
        asyncio.run(send_message(platform, target, message))

async def send_message(platform, target, message):
    try:
        if platform == 'discord':
            channel = discord_bot.get_channel(int(target))
            if channel:
                await channel.send(message)
                click.echo("Message sent to Discord successfully")
            else:
                click.echo("Discord channel not found")
        elif platform == 'telegram':
            await telegram_bot.send_message(chat_id=target, text=message)
            click.echo("Message sent to Telegram successfully")
    except Exception as e:
        click.echo(f"Error sending message: {str(e)}")

@cli.command()
@click.option('--platform', type=click.Choice(['discord', 'telegram']), required=True, help='Choose the platform to check status')
def status(platform):
    """Check the connection status of the specified platform."""
    if platform == 'discord':
        click.echo(f"Discord bot is {'connected' if discord_bot.is_ready() else 'disconnected'}")
    elif platform == 'telegram':
        try:
            info = telegram_bot.get_me()
            click.echo(f"Telegram bot is connected (Username: @{info.username})")
        except Exception:
            click.echo("Telegram bot is disconnected")

@cli.command()
def list_scheduled():
    """List all scheduled messages."""
    c.execute("SELECT * FROM messages WHERE scheduled_time > datetime('now')")
    scheduled_messages = c.fetchall()
    if scheduled_messages:
        for msg in scheduled_messages:
            click.echo(f"ID: {msg[0]}, Platform: {msg[1]}, Target: {msg[2]}, Content: {msg[3]}, Scheduled: {msg[4]}")
    else:
        click.echo("No scheduled messages")

@cli.command()
@click.argument('message_id', type=int)
def cancel_scheduled(message_id):
    """Cancel a scheduled message by its ID."""
    c.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()
    click.echo(f"Scheduled message with ID {message_id} has been cancelled")

@cli.command()
def generate_report():
    """Generate a basic engagement report."""
    # This is a placeholder. In a real implementation, you would query your database for actual metrics.
    click.echo("Engagement Report:")
    click.echo("Discord messages sent: 100")
    click.echo("Telegram messages sent: 150")
    click.echo("Total user interactions: 500")

@discord_bot.event
async def on_ready():
    logger.info(f'{discord_bot.user} has connected to Discord!')

@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user:
        return

    if message.content.startswith('!rights'):
        await message.channel.send(compose_advocacy_message())

def handle_telegram_message(update, context):
    if update.message.text == '/rights':
        context.bot.send_message(chat_id=update.effective_chat.id, text=compose_advocacy_message())

def main():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('rights', handle_telegram_message))
    
    scheduler.start()
    
    # Start the Discord bot
    discord_bot.run(DISCORD_TOKEN)
    
    # Start the Telegram bot
    updater.start_polling()
    
    cli()

if __name__ == '__main__':
    main()
