# whisper-asr

Test whister as ASR.

## Prerequisites

Python >= 3.10

### on MacOS using [Homebrew](https://brew.sh/)

``` shell
brew install ffmpeg
brew install portaudio
```

### Create Virtual Environment

``` shell
python -m venv venv
echo 'venv' > .gitignore
```

### Activate and Deactivate Virtual Environment

``` shell
source venv/bin/activate
```

``` shell
source deactivate
```

## Installation

``` shell
pip install -r requirements.txt
```

Backlog:

``` shell
pip install -U openai-whisper
pip install setuptools-rust
pip install pyaudio
```

### Freeze the requirements

``` shell
pip freeze > requirements.txt
```

## Example

### Run

``` shell
python example.py --audio_file_name=german           
Detected language: de
Detected text: Wie ist das weder ein Passwort?
Translated transcribt: How is the WLAN Password?
```

## Whisper API

### Enviroment Variables

[Whisper API](https://platform.openai.com/docs/api-reference/audio) needs API key from OpenAI as enviroment variables in `.env`:

``` shell
export OPENAI_API_KEY =
```

### Call API

``` shell
source .env
python whisper-api.py
python whisper-api.py --audio_file_name english --methode transcript  
python whisper-api.py --methode translate
```

## Server-Client

### run Server

``` shell
flask --app server run --port 5001
```

### run Client

``` shell
python client.py
python client.py --audio_file_name english
```

``` shell
curl -F "file=@audio/deutsch.mp3" http://localhost:5001/whisper
```

## Dockerize

``` shell
docker build . -t leonardmf/whisper-asr:0.2.1 -t leonardmf/whisper-asr:latest
docker run -p 5001:5000 leonardmf/whisper-asr:latest
docker run -p 8765:8765 leonardmf/whisper-asr:0.2.1

# with GPU
docker run --gpus=all -p 8765:8765 leonardmf/whisper-asr:0.2.1
docker run --gpus=all -p 5001:5000 leonardmf/whisper-asr:latest
```

``` shell
docker push leonardmf/whisper-asr:0.2.1
docker push leonardmf/whisper-asr:latest
```

``` shell
curl -F "file=@audio/deutsch.mp3" http://localhost:5001/whisper
```

## Audio

``` shell
ffmpeg -i input.m4a -vn -ar 44100 -ac 2 -b:a 192k output.mp3
```

## Streaming Server-Client

ASR with streaming and end-of-speech detection.

In terminal 1:

``` shell
python streaming_server.py
WebSocket server started. Listening on port 8765.
# Or docker
docker run -p 8765:8765 leonardmf/whisper-asr:0.2.1
# with GPU
docker run --gpus=all -p 8765:8765 leonardmf/whisper-asr:0.2.1
```

In terminal 2:

``` shell
python streaming_client.py
python streaming_client.py --task translate
python streaming_client.py --store-audio-flag True 
python streaming_client.py --audio_file_name 'audio/audio3.wav'
WebSocket connection established.
Start streaming audio ...
```

Start to speak ...
