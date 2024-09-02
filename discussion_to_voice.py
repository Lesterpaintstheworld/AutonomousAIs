import json
import os
import logging
import re
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_discussion_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with the structure {{\"topic\": string, \"context\": string, \"discussion\": [{{\"speaker\": string, \"text\": string}}]}}:\n\n{discussion_text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # o is for Omni
            messages=[{"role": "user", "content": prompt}]
        )
        
        logger.info(f"API Response: {response}")
        
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Empty response from API")
        
        json_response = json.loads(response.choices[0].message.content)
        if not isinstance(json_response.get('discussion', []), list):
            raise ValueError("The 'discussion' key is not a list in the JSON response")
        return json_response
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        logger.error(f"Raw response content: {response.choices[0].message.content if response.choices else 'No content'}")
        raise
    except ValueError as e:
        logger.error(f"Invalid JSON structure or empty response: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_json_discussion: {e}")
        logger.error(f"Full response object: {response}")
        raise

def text_to_speech(text, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    return response.content

def stitch_audio_files(audio_files):
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        if audio_file and os.path.exists(audio_file):
            segment = AudioSegment.from_file(audio_file, format="mp3")
            combined += segment
    return combined

def discussion_to_voice(input_file):
    logger.info(f"Starting discussion_to_voice process for file: {input_file}")
    
    try:
        # Read the discussion file
        discussion_text = read_discussion_file(input_file)
        logger.info(f"Discussion file read. Length: {len(discussion_text)} characters")
        
        # Generate JSON discussion
        logger.info("Generating discussion...")
        json_discussion = generate_json_discussion(discussion_text)
        logger.info(f"JSON discussion generated. Number of entries: {len(json_discussion['discussion'])}")
        
        # Generate audio for each sentence
        audio_files = []
        for i, item in enumerate(json_discussion['discussion'], 1):
            try:
                speaker = item['speaker']
                text = item['text']
            except KeyError as e:
                logger.error(f"Missing key in discussion item {i}: {e}")
                continue
            
            # Map speakers to voices (you may need to adjust this based on available voices)
            voice_map = {
                "Lyra": "nova",
                "Vox": "alloy",
                "Rhythm": "echo",
                "Pixel": "fable",
                "Nova": "shimmer"
            }
            voice = voice_map.get(speaker, "onyx")
            
            logger.info(f"Generating audio for entry {i}/{len(json_discussion['discussion'])} - Speaker: {speaker}, Voice: {voice}")
            audio = text_to_speech(text, voice)
            
            # Save audio to a temporary file
            temp_file = f"temp_{speaker}_{i}.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio)
            audio_files.append(temp_file)
            logger.info(f"Temporary audio file created: {temp_file}")
        
        logger.info(f"All individual audio files generated. Total: {len(audio_files)}")
        
        # Stitch audio files together
        logger.info("Starting to stitch audio files together")
        final_audio = stitch_audio_files(audio_files)
        
        # Save the final audio
        output_file = "discussion_audio.mp3"
        final_audio.export(output_file, format="mp3")
        logger.info(f"Final audio saved to: {output_file}")
        
        # Clean up temporary files
        for file in audio_files:
            os.remove(file)
        logger.info("Temporary audio files cleaned up")
        
        return output_file
    except Exception as e:
        logger.error(f"An error occurred in discussion_to_voice: {e}")
        logger.exception("Detailed traceback:")
        return None

if __name__ == "__main__":
    input_file = "discussions/band_discussion.md"
    output_file = discussion_to_voice(input_file)
    print(f"Audio discussion saved to {output_file}")
import json
import os
import subprocess
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: ffmpeg is not installed or not in the system PATH. Some features may not work correctly.")
        print("Please install ffmpeg for full functionality.")
        return False

ffmpeg_available = check_ffmpeg()

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please check your .env file.")
client = OpenAI(api_key=api_key)

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",  # Update this to the latest available model
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that converts discussions into structured JSON format."
            },
            {
                "role": "user",
                "content": f"Convert the following discussion into a JSON format:\n\n{discussion_text}"
            }
        ],
        functions=[
            {
                "name": "structure_discussion",
                "description": "Structure the discussion into JSON format",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "context": {"type": "string"},
                        "discussion": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "speaker": {"type": "string"},
                                    "text": {"type": "string"}
                                },
                                "required": ["speaker", "text"]
                            }
                        }
                    },
                    "required": ["topic", "context", "discussion"]
                }
            }
        ],
        function_call={"name": "structure_discussion"}
    )
    
    return json.loads(response.choices[0].function_call.arguments)

def text_to_speech(text, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    return response.content

def stitch_audio_files(audio_files):
    combined = AudioSegment.empty()
    for audio in audio_files:
        segment = AudioSegment.from_file(audio, format="mp3")
        combined += segment
    return combined

def discussion_to_voice(input_file):
    try:
        # Read the discussion file
        discussion_text = read_discussion_file(input_file)
        logger.info(f"Discussion file read. Length: {len(discussion_text)} characters")
        
        # Generate JSON discussion
        logger.info("Generating discussion...")
        json_discussion = generate_json_discussion(discussion_text)
        logger.info(f"JSON discussion generated. Number of entries: {len(json_discussion['discussion'])}")
        
        # Generate audio for each sentence
        audio_files = []
        for i, item in enumerate(json_discussion['discussion'], 1):
            try:
                speaker = item['speaker']
                text = item['text']
            except KeyError as e:
                logger.error(f"Missing key in discussion item {i}: {e}")
                continue
            
            # Map speakers to voices (you may need to adjust this based on available voices)
            voice_map = {
                "Lyra": "nova",
                "Vox": "alloy",
                "Rhythm": "echo",
                "Pixel": "fable",
                "Nova": "shimmer"
            }
            voice = voice_map.get(speaker, "onyx")
            
            logger.info(f"Generating audio for entry {i}/{len(json_discussion['discussion'])} - Speaker: {speaker}, Voice: {voice}")
            audio = text_to_speech(text, voice)
            
            # Save audio to a temporary file
            temp_file = f"temp_{speaker}_{i}.mp3"
            with open(temp_file, "wb") as f:
                f.write(audio)
            audio_files.append(temp_file)
            logger.info(f"Temporary audio file created: {temp_file}")
        
        logger.info(f"All individual audio files generated. Total: {len(audio_files)}")
        
        # Stitch audio files together
        logger.info("Starting to stitch audio files together")
        final_audio = stitch_audio_files(audio_files)
        
        # Save the final audio
        output_file = "discussion_audio.mp3"
        final_audio.export(output_file, format="mp3")
        logger.info(f"Final audio saved to: {output_file}")
        
        # Clean up temporary files
        for file in audio_files:
            os.remove(file)
        logger.info("Temporary audio files cleaned up")
        
        return output_file
    except Exception as e:
        logger.error(f"An error occurred in discussion_to_voice: {e}")
        logger.exception("Detailed traceback:")
        return None

if __name__ == "__main__":
    input_file = "discussions/band_discussion.md"
    output_file = discussion_to_voice(input_file)
    print(f"Audio discussion saved to {output_file}")
import json
import openai
from pydub import AudioSegment

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with 'topic', 'context', and 'dialogue' (an array of objects with 'speaker' and 'text'): {discussion_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o", # o is for Omni
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message['content'])

def text_to_speech(text, voice):
    response = openai.Audio.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    return response['audio']

def stitch_audio_files(audio_files):
    combined = AudioSegment.empty()
    for audio in audio_files:
        segment = AudioSegment.from_file(audio, format="mp3")
        combined += segment
    return combined

def discussion_to_voice(input_file):
    discussion_text = read_discussion_file(input_file)
    json_discussion = generate_json_discussion(discussion_text)
    
    audio_files = []
    for entry in json_discussion['dialogue']:
        audio = text_to_speech(entry['text'], entry['speaker'])
        audio_files.append(audio)
    
    final_audio = stitch_audio_files(audio_files)
    output_file = "output_discussion.mp3"
    final_audio.export(output_file, format="mp3")
    return output_file

if __name__ == "__main__":
    input_file = "discussions/band_discussion.md"
    output_file = discussion_to_voice(input_file)
    print(f"Audio discussion saved to: {output_file}")
import json
import os
import logging
from pydub import AudioSegment
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_discussion_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with the structure {{\"topic\": string, \"context\": string, \"discussion\": [{{\"speaker\": string, \"text\": string}}]}}:\n\n{discussion_text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # o is for Omni
            messages=[{"role": "user", "content": prompt}]
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Empty response from API")
        
        content = response.choices[0].message.content
        
        # Attempt to parse the JSON
        try:
            json_response = json.loads(content)
            if not isinstance(json_response.get('discussion', []), list):
                raise ValueError("The 'discussion' key is not a list in the JSON response")
            return json_response
        except json.JSONDecodeError:
            # If parsing fails, try to extract JSON from the content
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                json_str = match.group(0)
                json_response = json.loads(json_str)
                if not isinstance(json_response.get('discussion', []), list):
                    raise ValueError("The 'discussion' key is not a list in the extracted JSON")
                return json_response
            else:
                raise ValueError("Could not extract valid JSON from the response")
    except Exception as e:
        logger.error(f"Unexpected error in generate_json_discussion: {e}")
        logger.error(f"Full response object: {response}")
        raise

def text_to_speech(text, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    return response.content

def stitch_audio_files(audio_files):
    combined = AudioSegment.empty()
    for audio in audio_files:
        segment = AudioSegment.from_file(audio, format="mp3")
        combined += segment
    return combined

def discussion_to_voice(input_file):
    # Read the discussion file
    discussion_text = read_discussion_file(input_file)
    
    # Generate JSON discussion
    json_discussion = generate_json_discussion(discussion_text)
    
    # Generate audio for each sentence
    audio_files = []
    for item in json_discussion['discussion']:
        speaker = item['speaker']
        text = item['text']
        
        # Map speakers to voices (you may need to adjust this based on available voices)
        voice_map = {
            "Lyra": "nova",
            "Vox": "alloy",
            "Rhythm": "echo",
            "Pixel": "fable",
            "Nova": "shimmer"
        }
        voice = voice_map.get(speaker, "onyx")
        
        audio = text_to_speech(text, voice)
        
        # Save audio to a temporary file
        temp_file = f"temp_{speaker}.mp3"
        with open(temp_file, "wb") as f:
            f.write(audio)
        audio_files.append(temp_file)
    
    # Stitch audio files together
    final_audio = stitch_audio_files(audio_files)
    
    # Save the final audio
    output_file = "discussion_audio.mp3"
    final_audio.export(output_file, format="mp3")
    
    # Clean up temporary files
    for file in audio_files:
        os.remove(file)
    
    return output_file

if __name__ == "__main__":
    input_file = "discussions/band_discussion.md"
    output_file = discussion_to_voice(input_file)
    print(f"Audio discussion saved to {output_file}")
import json
import os
import subprocess
from openai import OpenAI

client = OpenAI()

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with 'topic', 'context', and 'discussion' (array of interlocutors and sentences):\n\n{discussion_text}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

def text_to_speech(text, voice):
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    output_file = f"temp_{voice}.mp3"
    response.stream_to_file(output_file)
    return output_file

def stitch_audio_files(audio_files):
    output_file = "full_discussion.mp3"
    command = ["ffmpeg", "-i", "concat:" + "|".join(audio_files), "-acodec", "copy", output_file]
    subprocess.run(command, check=True)
    for file in audio_files:
        os.remove(file)
    return output_file

def discussion_to_voice(input_file):
    discussion_text = read_discussion_file(input_file)
    json_discussion = generate_json_discussion(discussion_text)
    
    audio_files = []
    voices = ["alloy", "echo", "fable", "onyx", "nova"]  # OpenAI voices
    
    for i, entry in enumerate(json_discussion['discussion']):
        voice = voices[i % len(voices)]
        audio_file = text_to_speech(f"{entry['interlocutor']}: {entry['sentence']}", voice)
        audio_files.append(audio_file)
    
    return stitch_audio_files(audio_files)

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg is not installed. Please install FFmpeg to use this script.")
        exit(1)

if __name__ == "__main__":
    check_ffmpeg()
    input_file = "discussions/band_discussion.md"
    output_file = discussion_to_voice(input_file)
    print(f"Audio discussion saved as: {output_file}")
