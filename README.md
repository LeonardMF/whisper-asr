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

    source venv/bin/activate

    source deactivate

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

    pip freeze > requirements.txt

## Example

### Enviroment Variables

Whisper needs API key from OpenAI as enviroment variables in `.env`:

    export OPENAI_API_KEY =

## Run

``` shell
    python example.py --audio_file_name=german           
    Detected language: de
    Detected text: Wie ist das weder ein Passwort?
    Translated transcribt: How is the WLAN Password?
```
