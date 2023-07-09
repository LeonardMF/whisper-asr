# Konvertiert Huggingface Modell nach PyTorch Modell

import torch
import whisper
from multiple_datasets.hub_default_utils import convert_hf_whisper

device = "cuda" if torch.cuda.is_available() else "cpu"

# Write HF model to local whisper model
convert_hf_whisper("./whisper-tiny-de", "../assets/whisper-model.pt")

# Load the whisper model
model = whisper.load_model("../assets/whisper-model.pt", device=device)

# Transcribe arbitrarily long audio
# model.transcribe("long_audio.m4a", language="pt")["text"]
