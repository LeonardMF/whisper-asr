import asyncio
import aiofiles
import struct
import websockets
import time
import sounddevice as sd
import numpy as np
import asyncclick as click

from vad import MyEOS, VadAnalyzer

LOCAL_WEB_SOCKET_URL = "ws://127.0.0.1:8765"
DEFAULT_SAMPLE_RATE = "48000"
DEFAULT_CHANNELS = "1"
DEFAULT_DTYPE = np.int16
DEFAULT_TASK = "translate"
DEFAULT_AUDIO_FILE_NAME = "audio/audio.wav"
DEFAULT_CHUNK_SIZE = 1024
DEFAULT_STORE_AUDIO_FLAG = False

# Init EOS detector
# myEOS = MyEOS()
vadAnalyzer = VadAnalyzer(int(DEFAULT_SAMPLE_RATE))

async def audio_stream(
    samplerate       = DEFAULT_SAMPLE_RATE,
    channels         = DEFAULT_CHANNELS,
    dtype            = DEFAULT_DTYPE,
    task             = DEFAULT_TASK,
    url              = LOCAL_WEB_SOCKET_URL,
    store_audio_flag = DEFAULT_STORE_AUDIO_FLAG,
):
    samplerate = int(samplerate)
    channels   = int(channels)
    
    # Set the WebSocket request headers
    headers = {
        "samplerate": samplerate,
        "channels": channels,
        "dtype": dtype,
        "task": task,
        "store_audio_flag": store_audio_flag,
    }
    
    # Open the WebSocket connection
    async with websockets.connect(url,extra_headers=headers) as websocket:
        print("WebSocket connection established.")
    
        # Configure sounddevice input stream
        stream = sd.InputStream(
            channels=channels,
            samplerate=samplerate,
            dtype=np.int16,
        )
        
        # Start recording audio
        stream.start()
        print("Start streaming audio ...")
        
        while True:
            # Read audio data from input stream
            audio_data, _ = stream.read(1024)
            
            # Detect start of speech
            # end_of_speech_flag = myEOS.detect_end_of_speech(audio_data)
            audio = audio_data.tobytes()
            end_of_speech_flag = vadAnalyzer.detect_end_of_speech(audio)
    
            # Detect end of speech
            if end_of_speech_flag:
                stream.stop()
                print("Stop streaming audio ...")
                # send end of speech
                eos_time = time.time()
                await websocket.send("end of speech")
                break
            else: 
                # Send audio data to the WebSocket server
                await websocket.send(audio)
         
        # Receive any response from the WebSocket server (if needed)
        response = await websocket.recv()
        response_time = time.time()
        print(response)
        print("Response time: " + str(response_time - eos_time))
        await websocket.close()

async def audio_file_stream(
    samplerate       = DEFAULT_SAMPLE_RATE,
    channels         = DEFAULT_CHANNELS,
    dtype            = DEFAULT_DTYPE,
    task             = DEFAULT_TASK,
    url              = LOCAL_WEB_SOCKET_URL,
    store_audio_flag = DEFAULT_STORE_AUDIO_FLAG,
    audio_file_name  = DEFAULT_AUDIO_FILE_NAME,
):
    samplerate = int(samplerate)
    channels   = int(channels)
    
    # Set the WebSocket request headers
    headers = {
        "samplerate": samplerate,
        "channels": channels,
        "dtype": dtype,
        "task": task,
        "store_audio_flag": store_audio_flag,
    }
    
    # Open the WebSocket connection
    async with websockets.connect(url,extra_headers=headers) as websocket:
        print("WebSocket connection established.") 
    
        chunk_size = DEFAULT_CHUNK_SIZE
        
        print("Start streaming from audio file: " + audio_file_name)
        async with aiofiles.open(audio_file_name, 'rb') as afp:
            data = await afp.read(chunk_size)
            while data:
                await asyncio.sleep(0.01)
                await websocket.send(data)
                data = await afp.read(chunk_size)
            print("Send end of speech...")
            eos_time = time.time()
            await websocket.send("end of speech")
        
        response = await websocket.recv()
        response_time = time.time()
        print(response)
        print("Response time: " + str(response_time - eos_time))
        await websocket.close()

@click.command()
@click.option(
    "--task",
    default="transcribe",
    type=str,
    help="Task to perform: translate or transcribe",
)
@click.option(
    "--url",
    default=LOCAL_WEB_SOCKET_URL,
    type=str,
    help="URL of the WebSocket server",
) 
@click.option(
    "--samplerate",
    default="44100",
    type=str,
    help="Sample rate of the audio stream",
)
@click.option(
    "--channels",
    default="1",
    type=str,
    help="Channels of the audio stream",
)
@click.option(
    "--store-audio-flag",
    default=False,
    type=bool,
    help="Store audio file on server",
)
@click.option(
    "--audio_file_name",
    default="",
    type=str,
    help="name of the audio file to be streamed",
)
async def main(task: str, url: str, samplerate: str, channels: str, store_audio_flag: bool, audio_file_name: str):
    # Run the audio_stream function in an event loop
    if audio_file_name:
        await audio_file_stream(
            task=task,
            url=url,
            samplerate=samplerate,
            channels=channels,
            store_audio_flag=store_audio_flag,
            audio_file_name=audio_file_name)
    else:
        await audio_stream(
            task=task,
            url=url,
            samplerate=samplerate,
            channels=channels,
            store_audio_flag=store_audio_flag)

if __name__ == "__main__":
    asyncio.run(main())
