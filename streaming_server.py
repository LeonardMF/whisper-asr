#!/usr/bin/env python
import os
import asyncio
import websockets
import wave
import whisper
import time
import torch
import datetime
import randomname

# Check if NVIDIA GPU is available
print("NVIDIA GPU is available: " + str(torch.cuda.is_available()))
if torch.cuda.is_available():
    DEVICE = "cuda" 
else:
    DEVICE = "cpu"
# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)

async def audio_server(websocket):
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
    
    if "store_audio_flag" in headers and headers["store_audio_flag"] == "True":
        store_audio_flag = True
    else:
        store_audio_flag = False
    
    # Configure WAV file settings
    current_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-")
    wave_file_name = current_date + randomname.get_name() + ".wav"
    file_path = "audio/"
    wave_file = wave.open(file_path + wave_file_name, "wb")
    wave_file.setnchannels(channels)  
    wave_file.setsampwidth(2)  # 2 bytes per sample
    wave_file.setframerate(samplerate)

    try:
        while True:
            # Receive audio data from the WebSocket client
            audio_data = await websocket.recv()
            if isinstance(audio_data, bytes):
                # Write audio data to the WAV file
                wave_file.writeframes(audio_data)
            elif task == "translate":
                # Detect language
                audio = whisper.load_audio(file_path + wave_file_name)
                audio = whisper.pad_or_trim(audio)
                
                # make log-Mel spectrogram and move to the same device as the model
                detect_start_time = time.time()
                mel = whisper.log_mel_spectrogram(audio).to(model.device)
            
                # detect the spoken language
                _, probs = model.detect_language(mel)
                detected_language = max(probs, key=probs.get)
                detect_duration = time.time() - detect_start_time
                
                # Translate audio file
                translate_start_time = time.time()
                translate_result = model.transcribe(audio, task = 'translate', fp16=False)
                translate_duration = time.time() - translate_start_time
                await websocket.send(f"Translation: {translate_result['text']} (Duration: {translate_duration}) (Detected Language: {detected_language}) (Duration: {detect_duration})")
                break
            else:
                # Transcribe audio file
                transcribe_start_time = time.time()
                transcribe_result = model.transcribe(file_path + wave_file_name)
                transcribe_duration = time.time() - transcribe_start_time
                await websocket.send(f"Transcript: {transcribe_result['text']} (Duration: {transcribe_duration})")
                break
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed.")

    finally:
        # Close the WAV file
        wave_file.close()
        # Delete the WAV file
        if store_audio_flag == False:
            os.remove(file_path + wave_file_name)
            print("Audio file deleted: " + file_path + wave_file_name)
        else:
            print("Audio file saved: " + file_path + wave_file_name)

async def main():
    # Start the WebSocket server
    server = await websockets.serve(audio_server, "0.0.0.0", 8765)

    print("WebSocket server started. Listening on port 8765.")

    # Run the server indefinitely
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())