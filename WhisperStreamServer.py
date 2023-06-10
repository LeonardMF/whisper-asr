#!/usr/bin/env python

# WhisperStreamServer dient der Verarbeitung eines AudioStreams aus einer Websocket.


# extern

import logging
import json
import time
import wave
import asyncio
import websockets

import torch
import whisper


# whisper

from WhisperConst import WHISPER_LOG_LEVEL, WHISPER_DEFAULT_PORT, WHISPER_TEMP_FILE, WHISPER_DEFAULT_LANGUAGE, WHISPER_DEFAULT_SAMPLERATE, WHISPER_DEFAULT_CHANNELS, WHISPER_DEFAULT_DTYPE, WHISPER_TRANSLATE_TASK, WHISPER_TRANSCRIBE_TASK, WHISPER_DEFAULT_TASK
from WhisperVersion import WHISPER_BUILD, WHISPER_VERSION, WHISPER_DATE


# Logger

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(name)s | -> %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel( WHISPER_LOG_LEVEL )


# Versionsausgabe

logger.info(f"Whisper-ASR Server: Version {WHISPER_VERSION}.{WHISPER_BUILD} vom {WHISPER_DATE}")


# Check if NVIDIA GPU is available

logger.info(f"NVIDIA GPU is available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    DEVICE = "cuda" 
else:
    DEVICE = "cpu"


# Load the Whisper model:

model = whisper.load_model("base", device=DEVICE)


# Hauptfunktion zur Analyse eines Audio-Streams

async def audio_server(websocket, path):
    logger.debug("WebSocket connection established.")

    # Defaultwerte

    samplerate = WHISPER_DEFAULT_SAMPLERATE
    channels = WHISPER_DEFAULT_CHANNELS
    dtype = WHISPER_DEFAULT_DTYPE
    task = WHISPER_DEFAULT_TASK
    language = WHISPER_DEFAULT_LANGUAGE

    # einlesen der Header

    try:
        headers = websocket.request_headers
        logger.debug(f"Header: {headers}")

        if "samplerate" in headers:
            samplerate = int(headers["samplerate"])

        if "channels" in headers:
            channels = int(headers["channels"])

        if "dtype" in headers:
            dtype = headers["dtype"]

        if "task" in headers:
            task = headers["task"]

        if "language" in headers:
            language = headers["language"]
    except Exception as aException:
        logger.exception(f"audio_server: Exception {aException}")

    # Schleife zum Einlesen der Audiodaten

    wave_file = None
    try:
        # Configure WAV file settings

        wave_file = wave.open(WHISPER_TEMP_FILE, "wb")
        wave_file.setnchannels(channels)
        wave_file.setsampwidth(2)  # 2 bytes per sample
        wave_file.setframerate(samplerate)

        while True:
            # Receive audio data from the WebSocket client
            audio_data = await websocket.recv()
            if isinstance(audio_data, bytes):
                logger.debug(f"Receive Data: {len(audio_data)}")
                # Write audio data to the WAV file
                wave_file.writeframes(audio_data)
            elif task == "translate":
                logger.info("Translate...")
                # Detect language
                audio = whisper.load_audio( WHISPER_TEMP_FILE)
                audio = whisper.pad_or_trim( audio )
                
                # make log-Mel spectrogram and move to the same device as the model
                detect_start_time = time.time()
                mel = whisper.log_mel_spectrogram( audio ).to( model.device )
            
                # detect the spoken language
                _, probs = model.detect_language( mel )
                detected_language = max( probs, key=probs.get )
                detect_duration = time.time() - detect_start_time
                
                # Translate audio file
                translate_start_time = time.time()
                translate_result = model.transcribe(audio, task = 'translate', fp16=False)
                translate_duration = time.time() - translate_start_time
                logger.debug(f"Translation: result = {translate_result}  language = {detected_language}  duration = {detect_duration}")
                message = {
                    "type": "translate",
                    "text": translate_result['text'],
                    "language": detected_language,
                    "duration": translate_duration
                }
                await websocket.send( json.dumps( message ))
                break
            else:
                logger.info("Transcribe...")
                # Transcribe audio file
                transcribe_start_time = time.time()
                transcribe_result = model.transcribe( WHISPER_TEMP_FILE, language=language, fp16=False)
                transcribe_duration = time.time() - transcribe_start_time
                message = {
                    "type": "transcribe",
                    "text": transcribe_result['text'],
                    "language": language,
                    "duration": transcribe_duration
                }
                await websocket.send( json.dumps( message ))
                break

    except websockets.ConnectionClosed:
        logger.info("WebSocket connection closed.")

    finally:
        # Close the WAV file
        if wave_file is not None:
            wave_file.close()


# Hauptprogramm

async def main():
    # Start the WebSocket server
    server = await websockets.serve( audio_server, "0.0.0.0", WHISPER_DEFAULT_PORT)

    logger.info(f"WebSocket server started. Listening on port {WHISPER_DEFAULT_PORT}...")

    # Run the server indefinitely
    await server.wait_closed()
    logger.info("WebSocket server stoped.")


if __name__ == "__main__":
    asyncio.run(main())