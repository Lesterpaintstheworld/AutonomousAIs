import json
from pathlib import Path
from openai import OpenAI

client = OpenAI()

# Define character voices
character_voices = {
    "Lyra": "nova",
    "Rhythm": "onyx",
    "Vox": "shimmer",
    "Pixel": "fable",
    "Nova": "alloy"
}

# Load the discussion JSON
with open('discussions/first_steps_release_discussion.json', 'r') as f:
    discussion = json.load(f)

# Create a directory for the audio files if it doesn't exist
Path("audio_clips").mkdir(exist_ok=True)

# Generate voice clips for each message in the discussion
for i, message in enumerate(discussion['discussion']):
    speaker = message['speaker']
    text = message['message']
    voice = character_voices[speaker]
    
    speech_file_path = Path(f"audio_clips/{i+1:02d}_{speaker}.mp3")
    
    print(f"Generating audio for {speaker}...")
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )
    
    response.stream_to_file(speech_file_path)
    print(f"Audio saved to {speech_file_path}")

print("All audio clips generated successfully!")
