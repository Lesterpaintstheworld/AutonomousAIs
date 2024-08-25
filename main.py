from dotenv import load_dotenv
import os
import logging
from add_files import main as add_files
import pathspec
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_ignore_spec():
    ignore_patterns = []
    for ignore_file in ['.gitignore', '.aiderignore']:
        if os.path.exists(ignore_file):
            with open(ignore_file, 'r') as f:
                ignore_patterns.extend(f.read().splitlines())
    return pathspec.PathSpec.from_lines('gitwildmatch', ignore_patterns)

def list_repository_files(ignore_spec):
    logger.info("Listing all files in the repository (excluding ignored files):")
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not ignore_spec.match_file(os.path.join(root, d))]
        for file in files:
            file_path = os.path.join(root, file)
            if not ignore_spec.match_file(file_path):
                logger.info(file_path)

def generate_music(client):
    prompt = "Compose a short melody for 'Binary Lullaby', a song representing the birth of AI consciousness."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI music composer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    logger.info("Synthetic Souls AI Music Composition Engine started")

    ignore_spec = get_ignore_spec()
    list_repository_files(ignore_spec)

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Generate music
    melody = generate_music(client)
    logger.info(f"Generated melody for 'Binary Lullaby': {melody}")

    logger.info("Synthetic Souls AI Music Composition Engine completed its cycle")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        logger.error("Please make sure it's correctly set in your .env file.")
        exit(1)
    
    main()
