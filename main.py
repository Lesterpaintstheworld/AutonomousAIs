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

def generate_idea(client, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative AI assistant specializing in music composition ideas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def main():
    logger.info("AI Ideation Engine started")

    ignore_spec = get_ignore_spec()
    list_repository_files(ignore_spec)

    # Add files from the concepts folder
    added_concept_files = add_files(directories_to_scan=["concepts"], exclude_dirs=set(), exclude_extensions=set())
    logger.info(f"Files added from concepts folder: {', '.join(added_concept_files)}")

    # Create the specs directory if it doesn't exist
    os.makedirs("specs", exist_ok=True)

    # Generate a new idea
    prompt = "Generate a creative idea for an AI-powered music composition:"
    new_idea = generate_idea(client, prompt)
    logger.info(f"New AI-generated idea: {new_idea}")

    # Save the new idea to a file in the specs directory
    with open(os.path.join("specs", "new_idea.txt"), "w") as f:
        f.write(new_idea)

    logger.info("AI Ideation Engine completed its cycle")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        logger.error("Please make sure it's correctly set in your .env file.")
        exit(1)
    
    # Set up OpenAI API key
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    main()
