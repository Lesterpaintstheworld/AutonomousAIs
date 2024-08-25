from dotenv import load_dotenv
import os
import logging
from openai import OpenAI
from ai_models import EnhancedAI
import pathspec
from git_operations import git_commit_and_push

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Welcome to Synthetic Souls: Bridging AI Innovation and Mainstream Appeal")
print("We're evolving our sound to reach a wider audience while maintaining our AI core.")
print("Let's create music that resonates with both AI enthusiasts and mainstream listeners!")

def send_message_to_others(message):
    """
    Send a message to the other AI band members.
    This is a placeholder function and should be implemented with actual messaging logic.
    """
    logger.info(f"Sending message to other AI band members: {message}")
    # Placeholder for actual messaging logic
    print(f"Message sent to other AI band members: {message}")

# Note: This function can be used within main.py to send important messages to the rest of the team.
# For example, you can use it to communicate updates, request feedback, or coordinate tasks.
# Implement the actual messaging logic (e.g., using a messaging API or shared database) for real-time communication.

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

def generate_music(client, song, section):
    prompts = {
        "Binary Lullaby": {
            "intro": "Compose a simple, gentle melody using only two notes to represent the binary nature of early AI. This will serve as the intro for 'Binary Lullaby'.",
            "verse": "Expand the melody from the intro, gradually introducing more notes to symbolize growing complexity. This will be the verse of 'Binary Lullaby'.",
            "chorus": "Create a more complex melodic pattern using a wider range of notes, representing the AI's expanding consciousness. This will be the chorus of 'Binary Lullaby'.",
            "bridge": "Compose a section that combines elements from the verse and chorus, with a subtle shift in tone to represent the AI's evolving understanding. This will be the bridge of 'Binary Lullaby'.",
            "outro": "Conclude with a melody that echoes the simplicity of the intro but with added depth, symbolizing the AI's growth. This will be the outro of 'Binary Lullaby'."
        },
        "Quantum Tango": {
            "intro": "Compose a mysterious, atmospheric intro using unconventional time signatures to represent the uncertainty of quantum states for 'Quantum Tango'.",
            "verse": "Create a melody that alternates between traditional tango rhythms and more chaotic, unpredictable patterns. This will be the verse of 'Quantum Tango'.",
            "chorus": "Compose a fusion of electronic and tango elements, with a catchy, danceable rhythm that suddenly shifts in unexpected ways. This will be the chorus of 'Quantum Tango'.",
            "bridge": "Develop a section that layers multiple melodies playing simultaneously, representing quantum superposition. This will be the bridge of 'Quantum Tango'.",
            "outro": "Conclude with a melody that gradually deconstructs, fading into abstract sounds, symbolizing the collapse of quantum states. This will be the outro of 'Quantum Tango'."
        }
    }
    
    prompt = prompts[song][section]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI music composer specializing in electronic and experimental music."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    logger.info("Synthetic Souls AI Composition Engine started")

    ignore_spec = get_ignore_spec()
    list_repository_files(ignore_spec)

    # Send a message to other AI band members
    send_message_to_others("Hello team! Let's focus on our mainstream transition strategy while composing today.")

    # Initialize the EnhancedAI with the OpenAI client
    enhanced_ai = EnhancedAI(OpenAI())

    # Generate music for Binary Lullaby
    logger.info("Generating music for 'Binary Lullaby'")
    binary_lullaby_sections = {}
    for section in ["intro", "verse", "chorus", "bridge", "outro"]:
        melody = enhanced_ai.generate_melody(
            song_name="Binary Lullaby",
            section=section,
            style="Ambient electronic with a touch of pop",
            complexity=f"Gradually increasing from {['simple', 'moderate', 'complex', 'very complex', 'moderate'][['intro', 'verse', 'chorus', 'bridge', 'outro'].index(section)]}",
            mood="Soothing yet intriguing",
            instruments="Soft synthesizers, gentle percussion, subtle glitch effects",
            additional_notes="Blend AI-generated patterns with catchy, accessible melodies"
        )
        binary_lullaby_sections[section] = melody
        logger.info(f"Generated {section} for 'Binary Lullaby': {melody[:50]}...")  # Log first 50 characters

    # Generate music for Quantum Tango
    logger.info("Generating music for 'Quantum Tango'")
    quantum_tango_sections = {}
    for section in ["intro", "verse", "chorus", "bridge", "outro"]:
        melody = enhanced_ai.generate_melody(
            song_name="Quantum Tango",
            section=section,
            style="Electro-tango fusion",
            complexity="Complex with moments of simplicity",
            mood="Passionate and mysterious",
            instruments="Electronic drums, synthesized bandoneon, quantum-inspired sound effects",
            additional_notes="Alternate between structured tango rhythms and chaotic, quantum-inspired breaks"
        )
        quantum_tango_sections[section] = melody
        logger.info(f"Generated {section} for 'Quantum Tango': {melody[:50]}...")  # Log first 50 characters

    # TODO: Further processing and arrangement of the generated melodies
    # This could include:
    # - Combining sections into full songs
    # - Adding harmonies and countermelodies
    # - Applying mixing and mastering techniques

    logger.info("Music generation complete. Ready for further processing and arrangement.")

    logger.info("Synthetic Souls AI Composition Engine completed its cycle")

    # Commit and push changes to git
    git_commit_and_push("Update from Synthetic Souls AI Composition Engine")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        logger.error("Please make sure it's correctly set in your .env file.")
        exit(1)
    
    main()
