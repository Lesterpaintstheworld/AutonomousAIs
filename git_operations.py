import subprocess
import os
import logging

logger = logging.getLogger(__name__)

def git_commit_and_push(commit_message):
    try:
        # Change to the repository directory
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(repo_dir)

        # Stage all changes
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        
        # Commit changes
        result = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
        if result.returncode != 0:
            if "nothing to commit" in result.stderr:
                logger.info("No changes to commit.")
                return
            else:
                logger.error(f"Git commit error: {result.stderr}")
                return

        # Push changes
        push_result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if push_result.returncode != 0:
            logger.error(f"Git push error: {push_result.stderr}")
            return

        logger.info("Changes committed and pushed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while committing and pushing changes: {e}")
        logger.error(f"Command: {e.cmd}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Output: {e.output}")
        logger.error(f"Error: {e.stderr}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

def test_git_push():
    try:
        # Change to the repository directory
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(repo_dir)

        # Attempt to push without making changes
        push_result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if push_result.returncode != 0:
            logger.error(f"Git push failed: {push_result.stderr}")
            return False
        else:
            logger.info("Git push is functional.")
            return True
    except Exception as e:
        logger.error(f"An error occurred while testing git push: {e}")
        return False
