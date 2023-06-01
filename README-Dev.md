# Whisper ASR Server

Der Whisper ASR Server dient der Kapselung der Whisper ASR und der Anbindung des ASR-Dienstes über eine Websocket.


## Whisper-CPP

Die Whisper CPP Version ist eine schnellere Variante der Open-AI Whisper Version. Sie wird mit pywhisptercpp
als Python-Bibliothek eingebunden:

    $ pip install pywhispercpp


### Docker

Erzeugen eines Docker-Containers:

    docker build . -f Dockerfile-cpp -t onsei/whisper-asr:0.3.0
    docker run -p 8765:8765 --name whisper onsei/whisper-asr:0.3.0

mit GPU:

    docker run --gpus=all -p 8765:8765 onsei/whisper-asr:0.3.0


