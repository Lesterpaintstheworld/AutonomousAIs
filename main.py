from dotenv import load_dotenv
import os
import logging
from add_files import main as add_files

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("AI Ideation Engine started")

    # Log all files in the repository
    logger.info("Listing all files in the repository:")
    for root, dirs, files in os.walk('.'):
        for file in files:
            logger.info(os.path.join(root, file))

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
