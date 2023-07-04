# Whisper-ASR Konstanten


import logging


WHISPER_LOG_LEVEL = logging.INFO
# WHISPER_LOG_LEVEL = logging.DEBUG


# Konstanten

WHISPER_DEFAULT_PORT = 8765
WHISPER_DEFAULT_LANGUAGE = "en"
WHISPER_TEMP_FILE = "audio.wav"
WHISPER_DEFAULT_SAMPLERATE = 44100
WHISPER_DEFAULT_CHANNELS = 1
WHISPER_DEFAULT_DTYPE = "int16"
WHISPER_TRANSLATE_TASK = "translate"
WHISPER_TRANSCRIBE_TASK = "transcribe"
WHISPER_DEFAULT_TASK = WHISPER_TRANSCRIBE_TASK