from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os
import uuid

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)
audio = elevenlabs.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)

save_file_path = f"{uuid.uuid4()}.mp3"

with open(save_file_path, "wb") as f:
  for chunk in audio:
    if chunk:
      f.write(chunk)

print(f"{save_file_path}: A new audio file was saved successfully!")

