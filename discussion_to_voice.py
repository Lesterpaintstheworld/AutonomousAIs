import json
import openai
import os
from pydub import AudioSegment

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with the structure {{\"topic\": string, \"context\": string, \"discussion\": [{{\"speaker\": string, \"text\": string}}]}}:\n\n{discussion_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.choices[0].message.content)

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
from pydub import AudioSegment
from openai import OpenAI

def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("ffmpeg is not installed or not in the system PATH. Please install ffmpeg to use this script.")

check_ffmpeg()

# Set up OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set. Please set it before running this script.")
client = OpenAI(api_key=api_key)

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with the structure {{\"topic\": string, \"context\": string, \"discussion\": [{{\"speaker\": string, \"text\": string}}]}}:\n\n{discussion_text}"
    
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
import openai
from pydub import AudioSegment

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with 'topic', 'context', and 'dialogue' (an array of objects with 'speaker' and 'text'): {discussion_text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o",
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
import openai
import os
from pydub import AudioSegment

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def read_discussion_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def generate_json_discussion(discussion_text):
    prompt = f"Convert the following discussion into a JSON format with the structure {{\"topic\": string, \"context\": string, \"discussion\": [{{\"speaker\": string, \"text\": string}}]}}:\n\n{discussion_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.choices[0].message.content)

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
