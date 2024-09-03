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

# Stitch all audio files together
from pydub import AudioSegment

def stitch_audio_files(directory):
    audio_files = sorted([f for f in os.listdir(directory) if f.endswith('.mp3')])
    combined = AudioSegment.empty()
    for file in audio_files:
        sound = AudioSegment.from_mp3(os.path.join(directory, file))
        combined += sound
    return combined

combined_audio = stitch_audio_files("audio_clips")
output_file = "combined_discussion.mp3"
combined_audio.export(output_file, format="mp3")
print(f"Combined audio saved to {output_file}")
