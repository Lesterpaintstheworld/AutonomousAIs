from dotenv import load_dotenv
import os
import logging
from add_files import main as add_files
import fnmatch
import pathspec

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

def main():
    logger.info("AI Ideation Engine started")

    ignore_spec = get_ignore_spec()

    # Log all files in the repository, excluding ignored files
    logger.info("Listing all files in the repository (excluding ignored files):")
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not ignore_spec.match_file(os.path.join(root, d))]
        for file in files:
            file_path = os.path.join(root, file)
            if not ignore_spec.match_file(file_path):
                logger.info(file_path)

    # Add files from the concepts folder
    added_concept_files = add_files(directories_to_scan=["concepts"], exclude_dirs=set(), exclude_extensions=set())
    logger.info(f"Files added from concepts folder: {', '.join(added_concept_files)}")

    # Create the specs directory if it doesn't exist
    os.makedirs("specs", exist_ok=True)

    logger.info("AI Ideation Engine completed its cycle")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        logger.error("Please make sure it's correctly set in your .env file.")
        exit(1)
    
    main()
