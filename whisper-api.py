# Note: you need to be using OpenAI Python v0.27.0 for the code below to work

import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
audio_file= open("./audio/deutsch.mp3", "rb")

# transcript = openai.Audio.transcribe("whisper-1", audio_file)
# print("transcript: ", transcript.text)

translate = openai.Audio.translate("whisper-1", audio_file, target_language="en")
print("translate: ", translate.text)
