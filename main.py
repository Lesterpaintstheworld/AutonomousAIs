from dotenv import load_dotenv
import os
import logging
from ai_ideation_engine import EnhancedAIIdeationEngine
from add_files import main as add_files

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("AI Ideation Engine started")

    # Add files from the concepts folder
    added_concept_files = add_files(directories_to_scan=["concepts"], exclude_dirs=set(), exclude_extensions=set())
    logger.info(f"Files added from concepts folder: {', '.join(added_concept_files)}")

    # Initialize the AI Ideation Engine
    ideation_engine = EnhancedAIIdeationEngine()

    # Create the specs directory if it doesn't exist
    os.makedirs("specs", exist_ok=True)

    # Comment out other actions
    """
    # Generate new AI concepts
    new_concepts = ideation_engine.generate_ideas()

    # Develop specifications for the new concepts
    for concept in new_concepts:
        spec = ideation_engine.develop_specification(concept)
        safe_filename = "".join([c for c in concept if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        ideation_engine.save_specification(spec, f"specs/{safe_filename}.md")

    # Assess the feasibility of the new concepts
    for concept in new_concepts:
        feasibility = ideation_engine.assess_feasibility(concept)
        logger.info(f"Concept '{concept}' feasibility: {feasibility}")

    # Refine the concepts through collaborative sessions
    for concept in new_concepts:
        refined_concept = ideation_engine.refine_concept(concept)
        safe_filename = "".join([c for c in refined_concept if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        ideation_engine.save_specification(refined_concept, f"specs/{safe_filename}.md")

    # Run continuous improvement cycle
    improvement_suggestion = ideation_engine.run_continuous_improvement()
    logger.info(f"Continuous improvement suggestion: {improvement_suggestion}")
    """

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
