# einfacher Test des erstellen Whisper-Modells in Huggingface Transformers

from transformers import pipeline
import torch

# pruefen auf GPU

device = 0 if torch.cuda.is_available() else "cpu"


# Load the pipeline

transcribe = pipeline(
    task="automatic-speech-recognition",
    model="./whisper-tiny-de",
    chunk_length_s=30,
    device=device,
)

# Force model to transcribe in Portuguese
transcribe.model.config.forced_decoder_ids = transcribe.tokenizer.get_decoder_prompt_ids(language="pt", task="transcribe")

# Transcribe your audio file
for index in range(1, 54):
    print(f"Text(aida-kws-{index}): ", transcribe(f"./audio/aida-kws-{index}.wav")["text"])
