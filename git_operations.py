import subprocess
import logging

logger = logging.getLogger(__name__)

def git_commit_and_push(commit_message):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push changes
        subprocess.run(["git", "push"], check=True)
        
        logger.info("Successfully committed and pushed changes to git.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred during git operations: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
