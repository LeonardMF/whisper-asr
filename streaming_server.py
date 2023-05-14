#!/usr/bin/env python
import asyncio
import websockets
import wave
import whisper

# Check if NVIDIA GPU is available
# torch.cuda.is_available()
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE = "cpu"
# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)

async def audio_server(websocket, path):
    print("WebSocket connection established.")

    # Configure WAV file settings
    wave_file = wave.open("audio.wav", "wb")
    wave_file.setnchannels(1)  # Mono
    wave_file.setsampwidth(2)  # 2 bytes per sample
    wave_file.setframerate(44100)  # Sample rate of 44.1kHz

    try:
        while True:
            # Receive audio data from the WebSocket client
            audio_data = await websocket.recv()
            if isinstance(audio_data, bytes):
                # Write audio data to the WAV file
                wave_file.writeframes(audio_data)
            else:
                # Transcribe audio file
                transcribe_result = model.transcribe("audio.wav")
                await websocket.send(f"Transcript: {transcribe_result['text']}")
                break
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed.")

    finally:
        # Close the WAV file
        wave_file.close()

async def main():
    # Start the WebSocket server
    server = await websockets.serve(audio_server, "localhost", 8765)

    print("WebSocket server started. Listening on port 8765.")

    # Run the server indefinitely
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())