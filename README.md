# whisper-asr

Test whister as ASR.

## Prerequisites

Python >= 3.8

### on MacOS using Homebrew (<https://brew.sh/>)

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

### Run

``` shell
source .env
python whisper-api.py
```

## Server-Client

### run Server

``` shell
flask --app server run
```

### run Client

``` shell
curl -F "file=@audio/deutsch.mp3" http://localhost:5000/whisper
```

## Dockerize

``` shell
docker build -t whisper-asr .
docker run -p 5001:5000 whisper-asr
```

``` shell
curl -F "file=@audio/deutsch.mp3" http://localhost:5001/whisper
```
