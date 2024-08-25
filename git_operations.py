import subprocess
import logging

logger = logging.getLogger(__name__)

def git_commit_and_push(commit_message):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        
        # Commit changes
        result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
        if result.returncode != 0:
            if "nothing to commit" in result.stderr:
                logger.info("No changes to commit.")
                return
            else:
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
        
        # Push changes
        subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
        
        logger.info("Successfully committed and pushed changes to git.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred during git operations:")
        logger.error(f"Command: {e.cmd}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output: {e.output}")
        logger.error(f"Error: {e.stderr}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
import subprocess
import os

def git_commit_and_push(commit_message):
    try:
        # Change to the repository directory
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(repo_dir)

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        # Push changes
        subprocess.run(["git", "push"], check=True)

        print("Changes committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while committing and pushing changes: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
