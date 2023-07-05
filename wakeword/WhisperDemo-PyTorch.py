# einfacher Test des erstellen Whisper-Modells in PyTorch

import whisper
import torch


# pruefen auf GPU

device = 0 if torch.cuda.is_available() else "cpu"

model = whisper.load_model("../assets/whisper-model.pt")


def transcribe( aAudioFile: str ):
    # load audio and pad/trim it to fit 30 seconds
    result = model.transcribe( aAudioFile )
    return result["text"]


# run the transcribe with translation
# german_to_english = model.transcribe(audio, task='translate', fp16=False)

# print result
# print(f"Translated transcribt:{german_to_english['text']}")

# Transcribe your audio file
for index in range(1, 54):
    print(f"Text(aida-kws-{index}): ", transcribe(f"./audio/aida-kws-{index}.wav"))
