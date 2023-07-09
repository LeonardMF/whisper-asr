#!/usr/bin/env python

# Diese Server-Version greift auf pywhispercpp als Python-Bibliothek von whisper.cpp zu
# Dient dem Vergleich der CPP Version mit der Open-AI Version von Whisper
# Die Python-Anbindung beinhaltet nur Transcribe, nicht Translate.

import time
import json
import wave
import asyncio
import websockets
from pywhispercpp.model import Model


# Load the Whisper model:
model = Model(model="./assets/ggml-model.bin")


async def audio_server(websocket, path):
    print("WebSocket connection established.")
    headers = websocket.request_headers
    
    if "samplerate" in headers:
        samplerate = int(headers["samplerate"])
    else:
        samplerate = 44100 # Default 44.1 kHz
        
    if "channels" in headers:
        channels = int(headers["channels"])
    else:
        channels = 1 # Mono
        
    if "task" in headers:
        task = headers["task"]
    else:
        task = "transcribe"

    print(f"Header: {headers}")

    # Configure WAV file settings
    wave_file = wave.open("audio.wav", "wb")
    wave_file.setnchannels(channels)  
    wave_file.setsampwidth(2)  # 2 bytes per sample
    wave_file.setframerate(samplerate)

    try:
        while True:
            # Receive audio data from the WebSocket client
            audio_data = await websocket.recv()
            if isinstance(audio_data, bytes):
                print(f"Receive Data: {len(audio_data)}")
                # Write audio data to the WAV file
                wave_file.writeframes(audio_data)
            elif task == "transcribe":
                print("Transcribe...")

                # Translate audio file
                translate_start_time = time.time()
                segmentList = model.transcribe("audio.wav")
                translate_duration = time.time() - translate_start_time
                print(f"Translation: result = {segmentList}  duration = {translate_duration}")
                text = ""
                for segment in segmentList:
                    text += segment.text

                message = {
                    "text": text
                }

                await websocket.send( json.dumps( message ))
                break
            else:
                print("Translate...")
                print("ist nicht implementiert")
                break
    except websockets.ConnectionClosed:
        print("WebSocket connection closed.")


    finally:
        # Close the WAV file
        wave_file.close()


async def main():
    # Start the WebSocket server
    server = await websockets.serve(audio_server, "0.0.0.0", 8765)

    print("WebSocket server started. Listening on port 8765.")

    # Run the server indefinitely
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())