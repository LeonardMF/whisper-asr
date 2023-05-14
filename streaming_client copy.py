import asyncio
import websockets
import time
import sounddevice as sd
import numpy as np

WEB_SOCKET_URI = "ws://127.0.0.1:8765"

async def audio_stream():
    # Open the WebSocket connection
    async with websockets.connect(WEB_SOCKET_URI) as websocket:
        print("WebSocket connection established.")
    
        # Configure sounddevice input stream
        stream = sd.InputStream(
            channels=1,
            samplerate=44100,
            dtype=np.int16,
        )
        
        # Start recording audio
        stream.start()
        print("Start streaming audio ...")
        
        start_time = time.time()
        
        while True:
            # Read audio data from input stream
            audio_data, _ = stream.read(1024)
            
            # ToDo: Detect end of speech
            
            # Send audio data to the WebSocket server
            await websocket.send(audio_data.tobytes())
            # Check if 5 seconds have elapsed
            if time.time() - start_time >= 5:
                stream.stop()
                print("Stop streaming audio ...")
                # send end of speech
                await websocket.send("end of speech")
                break
         
        # Receive any response from the WebSocket server (if needed)
        response = await websocket.recv()
        
        print(response)
        
        await websocket.close()
          
async def main():
    # Run the audio_stream function in an event loop
    await audio_stream()

if __name__ == "__main__":
    asyncio.run(main())
