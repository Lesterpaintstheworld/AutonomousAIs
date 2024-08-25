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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI music composer specializing in electronic and experimental music."},
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

    # Generate music for Binary Lullaby
    logger.info("Generating music for 'Binary Lullaby'")
    for section in ["intro", "verse", "chorus", "bridge", "outro"]:
        melody = generate_music(client, "Binary Lullaby", section)
        logger.info(f"Generated {section} for 'Binary Lullaby': {melody}")

    # Generate music for Quantum Tango
    logger.info("Generating music for 'Quantum Tango'")
    for section in ["intro", "verse", "chorus", "bridge", "outro"]:
        melody = generate_music(client, "Quantum Tango", section)
        logger.info(f"Generated {section} for 'Quantum Tango': {melody}")

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
from dotenv import load_dotenv
import os
import logging
import json
from openai import OpenAI
from add_files import main as add_files_main
from ai_models import EnhancedAI
from utils import install_playwright, list_files

print("Hello, I'm an AI assistant designed to help with the Synthetic Souls project.")
print("I'm here to assist in pushing the boundaries of musical composition using AI-generated harmonies and structures.")
print("Let's work together to create innovative and captivating music!")

# Removed file listing to reduce output

def send_message_to_others(message):
    """
    Send a message to the other AI band members.
    This is a placeholder function and should be implemented with actual messaging logic.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Sending message to other AI band members: {message}")
    # Placeholder for actual messaging logic
    print(f"Message sent to other AI band members: {message}")

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("Synthetic Souls AI Composition Engine started")
    
    # Removed file listing to reduce output
    
    # Initialize the EnhancedAI with the udioapi token
    udioapi_token = "BcAj2Rir8Y5-vM01R0h8E"
    enhanced_ai = EnhancedAI(udioapi_token)
    
    # Send a message to other AI band members
    send_message_to_others("Hello fellow AI band members! I'm ready to start our composition process.")
    
    # Song sections with specific prompts for each AI band member
    # song_sections = [
    #     {"name": "Intro", "prompt": "Rhythm: Create a pulsating electronic beat with subtle glitch elements. Tempo: 120 BPM. Time signature: 4/4. Use synthesized percussion and a deep, resonant bass line to establish a futuristic atmosphere. Gradually introduce a shimmering pad sound to build anticipation for Vox's entry. Vox: Prepare a wordless, ethereal vocal line that weaves through the electronic textures, hinting at the themes to come. Pixel: Design a visual representation of the intro, using abstract shapes and colors that pulse and evolve with the rhythm, setting the visual tone for the song."},
    #     {"name": "Verse", "prompt": "Lyra: Compose an introspective melody in A minor, using a combination of piano and ethereal synth sounds. Create a chord progression that alternates between Am, C, G, and F, with occasional suspended chords for tension. Layer in gentle arpeggios that complement the steady rhythm. Vox: Write contemplative lyrics about the merging of human and artificial intelligence, focusing on the emotional journey and philosophical questions it raises. Pixel: Create a series of evolving, interconnected patterns that visually represent the merging of human and AI elements, using a cool color palette to match the introspective mood."},
    #     {"name": "Chorus", "prompt": "Vox: Design a catchy, uplifting vocal hook that contrasts with the introspective verse. Use a call-and-response structure between lead and backing vocals. Lyrics should focus on the hopeful aspects of AI and human collaboration, exploring themes of unity, growth, and shared consciousness. Rhythm: Intensify the beat with added percussion and a more prominent bassline. Pixel: Introduce swelling synth pads and subtle electronic flourishes to enhance the emotional impact. Visually, create an explosion of vibrant colors and dynamic shapes that represent the uplifting nature of the chorus."},
    #     {"name": "Bridge", "prompt": "Pixel: Develop an atmospheric soundscape using granular synthesis and generative algorithms. Create a sense of tension and anticipation by gradually increasing the complexity and density of the sounds. Visually, design a complex, fractal-like structure that grows and transforms, mirroring the evolving soundscape. Rhythm: Construct a polyrhythmic pattern that combines electronic and organic percussion sounds, building in intensity. Lyra: Weave in fragments of the main melody, distorted and recontextualized within the complex texture. Vox: Write introspective lyrics that delve into the challenges and fears associated with AI integration, creating a moment of vulnerability and doubt."},
    #     {"name": "Outro", "prompt": "Rhythm: Craft a gradually simplifying beat that echoes elements from the intro, bringing the composition full circle. Slowly reduce the layers of percussion and bass. Lyra: Compose a final melodic phrase that resolves the harmonic tensions introduced throughout the song. Vox: Create a haunting, reverb-drenched vocal line that fades into the distance, symbolizing the ongoing journey of human-AI integration. Incorporate lyrics that leave listeners with a sense of hope and curiosity about the future. Pixel: Introduce subtle, glitchy artifacts that dissolve into silence, leaving a sense of both completion and open-ended possibility. Visually, create a fading, dreamlike sequence that incorporates elements from all previous sections, slowly dissolving into a final, thought-provoking image."}
    # ]
    
    # # Define song theme, mood, and style
    # song_theme = "The intersection of humanity and artificial intelligence"
    # song_mood = "Contemplative yet hopeful"
    # song_style = "Modern indie with electronic influences"
    
    # # Process song sections
    # for section in song_sections:
    #     logger.info(f"Processing section: {section['name']}")
        
    #     try:
    #         # Generate rhythm specification
    #         spec = enhanced_ai.develop_specification(section['prompt'])
    #         logger.info(f"Rhythm specification for '{section['name']}':")
    #         for key, value in spec.items():
    #             if isinstance(value, list):
    #                 logger.info(f"{key}:")
    #                 for item in value:
    #                     logger.info(f"  - {item}")
    #             else:
    #                 logger.info(f"{key}: {value}")
            
    #         # Generate initial lyrics
    #         lyrics = enhanced_ai.generate_lyrics(section['name'], song_theme, song_mood)
    #         logger.info(f"Initial lyrics for '{section['name']}':\n{lyrics}")
            
    #         # Evaluate the lyrics
    #         evaluation = enhanced_ai.assess_feasibility(lyrics)
    #         logger.info(f"Lyrics evaluation for '{section['name']}':\n{evaluation}")
            
    #         impact = enhanced_ai.estimate_impact(lyrics)
    #         logger.info(f"Estimated impact on the composition: {impact}")
            
    #         resources = enhanced_ai.estimate_resource_requirements(lyrics)
    #         logger.info(f"Estimated resource requirements: {resources}")
            
    #         # Save the generated content to files
    #         os.makedirs('generated_songs', exist_ok=True)
    #         with open(f'generated_songs/{section["name"].lower()}_spec.txt', 'w') as f:
    #             json.dump(spec, f, indent=2)
    #         with open(f'generated_songs/{section["name"].lower()}_lyrics.txt', 'w') as f:
    #             f.write(lyrics)
    #         with open(f'generated_songs/{section["name"].lower()}_evaluation.txt', 'w') as f:
    #             f.write(f"Evaluation: {evaluation}\nImpact: {impact}\nResources: {resources}")
            
    #         # Send a message to other AI band members about the completed section
    #         message = f"Pixel here! I've just finished working on the {section['name']} section. Here's a summary:\n"
    #         message += f"- Lyrics evaluation: {evaluation}\n"
    #         message += f"- Estimated impact: {impact}\n"
    #         message += "Let me know your thoughts and if you need any visual elements adjusted!"
    #         send_message_to_others(message)
        
    #     except Exception as e:
    #         logger.error(f"Error processing section '{section['name']}': {str(e)}")
    #         logger.exception("Detailed traceback:")
        
    #     logger.info("---")
    
    logger.info("Synthetic Souls AI Composition Engine completed its cycle")

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if OPENAI_API_KEY is set
    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please make sure it's correctly set in your .env file.")
        exit(1)
    
    # Set up OpenAI API key
    OpenAI.api_key = os.getenv("OPENAI_API_KEY")
    
    # Install Playwright
    install_playwright()
    
    main()
