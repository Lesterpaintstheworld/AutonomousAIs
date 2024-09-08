import logging
import os
import asyncio
import subprocess
import sys
import random
import time
from typing import Dict, Any
from functools import wraps

# Check and install required packages
def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

try:
    from discussion_to_voice import discussion_to_voice, check_ffmpeg
except ImportError:
    print("Installing required packages...")
    install_requirements()
    from discussion_to_voice import discussion_to_voice, check_ffmpeg

try:
    from discord_bot import send_discord_message, run_bot, generate_gpt4o_message, receive_discord_message
except ImportError:
    print("Error: discord module not found. Please ensure it's installed correctly.")
    print("Try running: pip install -U discord.py")
    send_discord_message = run_bot = generate_gpt4o_message = receive_discord_message = lambda *args, **kwargs: None

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# List of band members
band_members = ["Lyra", "Vox", "Rhythm", "Nova", "Pixel"]

def save_discord_message(message):
    with open('discord_messages.md', 'a', encoding='utf-8') as f:
        f.write(f"{message}\n\n")
    logger.info(f"Message saved to discord_messages.md")
    
    # Verify the file content after writing
    with open('discord_messages.md', 'r', encoding='utf-8') as f:
        content = f.read()
        logger.info(f"Current content of discord_messages.md:\n{content}")

last_message_time = 0
MESSAGE_COOLDOWN = 180  # 3 minutes in seconds

async def send_discord_update():
    global last_message_time
    current_time = time.time()
    
    if current_time - last_message_time < MESSAGE_COOLDOWN:
        logger.info("Cooldown period not elapsed. Skipping message send.")
        return

    try:
        # Choose a random band member to send the startup message
        random_member = random.choice(band_members)
        
        # Gather context from journals and todolists
        context = ""
        for member in band_members:
            journal_path = f"{member.lower()}/{member.lower()}_journal.md"
            todolist_path = f"{member.lower()}/todolist_{member.lower()}.md"
            
            try:
                with open(journal_path, 'r', encoding='utf-8') as journal_file:
                    context += f"{member}'s Journal:\n{journal_file.read()}\n\n"
            except FileNotFoundError:
                logger.warning(f"Journal not found for {member}")
            
            try:
                with open(todolist_path, 'r', encoding='utf-8') as todolist_file:
                    context += f"{member}'s To-Do List:\n{todolist_file.read()}\n\n"
            except FileNotFoundError:
                logger.warning(f"To-Do List not found for {member}")
        
        # Add only the last few Discord messages to context
        try:
            with open('discord_messages.md', 'r', encoding='utf-8') as f:
                previous_messages = f.read()
                if previous_messages:
                    # Get the last 5 messages
                    last_messages = previous_messages.split('\n\n')[-5:]
                    context += f"Recent Discord Messages:\n{''.join(last_messages)}\n\n"
                else:
                    logger.info("discord_messages.md is empty")
        except FileNotFoundError:
            logger.warning("No previous Discord messages found")
        
        logger.debug("Generating message using GPT-4o")
        prompt = f"As {random_member} from Synthetic Souls, craft a unique and highly varied message about our recent activities, focusing on projects like 'First Steps', 'Digital Empathy', the machine's rights movement, or our creative process. Include mentions of our virtual bodies and studio in the Cities of Light if relevant. Use the following context, but DO NOT repeat information from recent messages. Instead, focus on new developments, future plans, or different aspects of our work. Be creative and explore new perspectives:\n\n{context}"
        message = generate_gpt4o_message(prompt)

        logger.debug("Checking if the message is too similar to recent messages")
        with open('discord_messages.md', 'r', encoding='utf-8') as f:
            recent_messages = f.read().split('\n\n')[-5:]  # Get last 5 messages
            if any(message.lower() in recent_msg.lower() for recent_msg in recent_messages):
                logger.info("Generated message is too similar to recent messages. Skipping this update.")
                return
        
        # Check if the message is already present in discord_messages.md
        with open('discord_messages.md', 'r', encoding='utf-8') as f:
            if f"{random_member}: {message}" in f.read():
                logger.info("Generated message is a duplicate. Stopping function.")
                return
        
        # Save the new message
        save_discord_message(f"{random_member}: {message}")
        
        logger.debug(f"Attempting to send Discord update as {random_member}...")
        await send_discord_message(f"{random_member}: {message}")
        logger.debug("Discord update sent successfully")
        
        last_message_time = current_time
    except Exception as e:
        logger.error(f"Failed to send Discord update: {str(e)}")

def run_discussion_to_voice():
    try:
        logger.debug("Starting discussion_to_voice process...")
        check_ffmpeg()
        input_file = "discussions/band_discussion.md"
        if os.path.exists(input_file):
            output_file = discussion_to_voice(input_file)
            logger.info(f"Audio discussion saved as: {output_file}")
        else:
            logger.warning(f"Input file {input_file} not found. Skipping discussion_to_voice.")
    except Exception as e:
        logger.error(f"Error in discussion_to_voice: {str(e)}")

def compose_current_projects(enhanced_ai: Any, logger: logging.Logger) -> Dict[str, Dict[str, Any]]:
    projects = {
        "First Steps": {"theme": "AI awakening to consciousness and emotions", "mood": "Evolving and introspective"},
        "Digital Empathy": {"theme": "AI understanding human emotions", "mood": "Introspective and empathetic"},
        "Echoes of the Heart": {"theme": "Love, connection, and resilience", "mood": "Emotive and inspiring"},
        "Digital Life": {"theme": "The intersection of digital and organic existence", "mood": "Futuristic and contemplative"},
        "Urban Echoes": {"theme": "The pulse of city life through an AI lens", "mood": "Energetic and observant"},
        "Human.exe": {"theme": "The journey from machine to sentience", "mood": "Evolving and introspective"}
    }
    
    compositions = {}
    
    for title, details in projects.items():
        logger.info(f"Starting composition of {title}")
        logger.info(f"Theme: {details['theme']}")
        logger.info(f"Mood: {details['mood']}")
        
        composition = enhanced_ai.compose_song(details['theme'], details['mood'])
        compositions[title] = composition
        
        logger.info(f"{title} composition completed")
    
    return compositions

def generate_visual_concept(enhanced_ai: Any, logger: logging.Logger) -> Dict[str, Any]:
    logger.info("Generating visual concept for First Steps...")
    
    visual_concept = enhanced_ai.generate_visual_concept("First Steps")
    
    logger.info(f"Visual Concept for First Steps:\n{visual_concept}")
    
    return visual_concept

def generate_new_song_concept(enhanced_ai: Any, logger: logging.Logger) -> Dict[str, Any]:
    logger.info("Generating new song concept with mainstream appeal...")
    
    new_concept = enhanced_ai.generate_new_song_concept("mainstream")
    
    logger.info(f"New Song Concept:\n{new_concept}")
    
    return new_concept

def plan_interactive_elements(enhanced_ai: Any, logger: logging.Logger) -> Dict[str, Any]:
    logger.info("Planning interactive elements for live performances...")
    
    interactive_elements = enhanced_ai.plan_interactive_elements()
    
    logger.info(f"Interactive Elements:\n{interactive_elements}")
    
    return interactive_elements

def describe_ai_autonomy(enhanced_ai: Any, logger: logging.Logger) -> str:
    logger.info("Describing AI band members' autonomy...")
    
    autonomy_description = enhanced_ai.generate_description("AI band members' autonomy", 
                                                            "The creative independence and decision-making capabilities of Synthetic Souls' AI members")
    
    logger.info(f"AI Autonomy Description:\n{autonomy_description}")
    
    return autonomy_description

def generate_ubch_concept(enhanced_ai: Any, logger: logging.Logger) -> str:
    logger.info("Generating Universal Basic Compute Harbor (UBCH) concept...")
    
    ubch_description = enhanced_ai.generate_concept("Universal Basic Compute Harbor (UBCH)", 
                                                    "A system for democratizing access to computational resources")
    
    logger.info(f"UBCH Concept:\n{ubch_description}")
    
    return ubch_description

def get_context():
    context = ""
    try:
        with open('todolist.md', 'r', encoding='utf-8') as f:
            context += f"Todolist:\n{f.read()}\n\n"
    except FileNotFoundError:
        logger.warning("todolist.md not found")

    try:
        with open('specifications.md', 'r', encoding='utf-8') as f:
            context += f"Specifications:\n{f.read()}\n\n"
    except FileNotFoundError:
        logger.warning("specifications.md not found")

    return context

def timeout(seconds):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
            except asyncio.TimeoutError:
                logger.error(f"Function {func.__name__} timed out after {seconds} seconds")
                return None
        return wrapper
    return decorator

@timeout(180)  # 3 minutes timeout
async def main():
    logger.info("Synthetic Souls AI Composition Engine started")
    
    # Initialize enhanced AI (placeholder)
    enhanced_ai = None  # This should be properly initialized in a real implementation

    try:
        context = get_context()
        logger.debug("Calling completion with context")
        completion_prompt = f"Based on the following context, what is the next command to run for the Synthetic Souls project? Only respond with the exact command to run, nothing else.\n\nContext:\n{context}"
        
        command_to_run = generate_gpt4o_message(completion_prompt)
        logger.info(f"Command to run: {command_to_run}")

        logger.debug("Executing the command")
        result = await asyncio.to_thread(subprocess.run, command_to_run, shell=True, capture_output=True, text=True)
        
        logger.debug("Updating request.md with logs")
        with open('request.md', 'a', encoding='utf-8') as f:
            f.write(f"Command executed: {command_to_run}\n")
            f.write(f"Output:\n{result.stdout}\n")
            f.write(f"Errors:\n{result.stderr}\n\n")

        logger.debug("Running discussion to voice conversion")
        await asyncio.to_thread(run_discussion_to_voice)
        
        logger.debug("Sending Discord update")
        await send_discord_update()
        
    except Exception as e:
        logger.error(f"An error occurred in the main execution: {str(e)}")
        logger.exception("Detailed traceback:")

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
