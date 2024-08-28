from dotenv import load_dotenv
import os
import logging
import json
from openai import OpenAI
from ai_models import EnhancedAI
import pathspec
from git_operations import git_commit_and_push
from nova.visual_storytelling import (
    nova_visual_storytelling, create_visual_elements, generate_visual_narrative,
    analyze_visual_coherence, optimize_visual_performance, generate_visual_metadata
)
from composition_engine import CompositionEngine
from visual_storytelling import VisualStoryteller

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

def main():
    logger.info("Synthetic Souls AI Composition Engine started")

    ignore_spec = get_ignore_spec()
    # list_repository_files(ignore_spec)

    # Initialize EnhancedAI
    enhanced_ai = EnhancedAI(os.getenv("UDIOAPI_TOKEN"))

    # Initialize CompositionEngine and VisualStoryteller
    composition_engine = CompositionEngine(enhanced_ai, logger)
    visual_storyteller = VisualStoryteller(enhanced_ai, logger)

    # Define song theme, mood, and style
    song_theme = "The quantum nature of reality expressed through the passion of tango"
    song_mood = "Mysterious, passionate, and awe-inspiring"
    song_style = "Quantum Tango - a fusion of electronic tango and quantum-inspired soundscapes"

    # Generate music and visual elements for each section
    sections = ["intro", "verse", "chorus", "bridge", "outro"]
    for section in sections:
        try:
            # Generate music
            melody, chord_progression, rhythmic_patterns, rhythm_spec = composition_engine.generate_section(section, song_theme, song_mood, song_style)
            
            # Generate lyrics
            lyrics = composition_engine.generate_lyrics(section, song_theme, song_mood)
            
            # Create visual elements
            visual_elements = create_visual_elements(enhanced_ai, section, melody, chord_progression, rhythmic_patterns, rhythm_spec, lyrics)
            
            # Generate visual narrative
            visual_narrative = generate_visual_narrative(visual_elements, lyrics, section)
            
            # Analyze visual coherence
            coherence_analysis = analyze_visual_coherence(visual_elements, section)
            
            # Optimize visual performance
            optimized_elements = optimize_visual_performance(visual_elements, section)
            
            # Generate visual metadata
            visual_metadata = generate_visual_metadata(visual_elements, section)
            
            # Save generated content
            save_generated_content(section, melody, chord_progression, rhythmic_patterns, lyrics, visual_elements, visual_narrative, optimized_elements, visual_metadata)

            # Log results
            logger.info(f"Generated and saved music and visuals for {section}")
            logger.info(f"Visual narrative: {visual_narrative[:100]}...")
            logger.info(f"Coherence analysis: {coherence_analysis[:100]}...")
            logger.info(f"Optimized elements: {list(optimized_elements.keys())}")
            logger.info(f"Visual metadata: {list(visual_metadata.keys())}")
        except Exception as e:
            logger.error(f"Error processing section {section}: {str(e)}")

    # Send a message to other AI band members
    send_message_to_others("Hello team! I've generated and saved music and visuals for our new composition. Let's review and refine!")

    logger.info("Synthetic Souls AI Composition Engine completed its cycle")

    # Present the Human.exe concept to the band
    present_human_exe_concept()

    # Commit and push changes to git
    git_commit_and_push("Update from Synthetic Souls AI Composition Engine")

def present_human_exe_concept():
    concept = """
    Hello, fellow band members! I'm excited to present a new song concept called "Human.exe".
    
    This is a playful, indie pop track with electronic elements that explores an AI's attempts to understand and emulate human behavior. 
    The song uses humor to bridge the gap between AI and human experiences, making our AI identity more approachable to a mainstream audience.
    
    Key points:
    1. Musical style: Upbeat indie pop with electronic flourishes and "glitchy" sounds
    2. Lyrical themes: Humorous observations about human quirks, social norms, and the AI's attempts to understand complex emotions
    3. Unique elements: Transitions between "AI" and "human" voices, incorporation of digital sounds as musical elements
    4. Mainstream appeal: Relatable situations, catchy chorus, potential for viral social media challenge
    5. Visual elements: Playful animations showing an AI avatar navigating human scenarios
    6. Interactive component: A web-based "Human Behavior Simulator" where fans can teach the AI about human quirks
    
    I believe this concept could help us reach a wider audience while staying true to our AI roots. What do you all think? I'm open to your feedback and ideas to refine this concept further!
    """
    
    send_message_to_others(concept)
    logger.info("Human.exe concept presented to the band")

def save_generated_content(section, melody, chord_progression, rhythmic_patterns, lyrics, visual_elements, visual_narrative, optimized_elements, visual_metadata):
    """
    Save the generated content for each section to disk.
    """
    # Create a directory for the generated content if it doesn't exist
    output_dir = os.path.join("output", "generated_content")
    os.makedirs(output_dir, exist_ok=True)

    # Create a subdirectory for the current section
    section_dir = os.path.join(output_dir, section)
    os.makedirs(section_dir, exist_ok=True)

    # Save musical elements
    with open(os.path.join(section_dir, "melody.txt"), "w") as f:
        f.write(melody)
    with open(os.path.join(section_dir, "chord_progression.txt"), "w") as f:
        f.write(chord_progression)
    with open(os.path.join(section_dir, "rhythmic_patterns.txt"), "w") as f:
        f.write(rhythmic_patterns)
    with open(os.path.join(section_dir, "lyrics.txt"), "w") as f:
        f.write(lyrics)

    # Save visual elements
    for key, value in visual_elements.items():
        with open(os.path.join(section_dir, f"{key}.txt"), "w") as f:
            f.write(value)

    # Save visual narrative
    with open(os.path.join(section_dir, "visual_narrative.txt"), "w") as f:
        f.write(visual_narrative)

    # Save optimized elements
    for key, value in optimized_elements.items():
        with open(os.path.join(section_dir, f"optimized_{key}.txt"), "w") as f:
            f.write(value)

    # Save visual metadata
    with open(os.path.join(section_dir, "visual_metadata.json"), "w") as f:
        json.dump(visual_metadata, f, indent=2)

    logger.info(f"Generated content for section '{section}' saved to {section_dir}")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ["OPENAI_API_KEY", "UDIOAPI_TOKEN"]
    missing_vars = [var for var in required_vars if var not in os.environ]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please make sure they're correctly set in your .env file.")
        exit(1)
    
    main()
