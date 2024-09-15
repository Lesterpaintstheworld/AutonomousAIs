import logging
import asyncio
import subprocess
from discord_bot import generate_gpt4o_message

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

async def main():
    logger.info("Synthetic Souls AI Composition Engine started")

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
        
    except Exception as e:
        logger.error(f"An error occurred in the main execution: {str(e)}")
        logger.exception("Detailed traceback:")

if __name__ == "__main__":
    asyncio.run(main())
