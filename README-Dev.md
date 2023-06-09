# Whisper ASR Server

Der Whisper ASR Server dient der Kapselung der Whisper ASR und der Anbindung des ASR-Dienstes über eine Websocket.



## Whisper-Python

Die Whisper-Python Version ist die offizielle Version von Open-AI mit deren Python-API und einem Websocket-Server.

### Docker

Fuer diese Version von Whisper werden zwei Docker-Container erzeugt. Der Whisper-Base Container enthält alle
Python-Installationen. Der Whisper-Server Container enthaelt den Whisper-Server Code. Damit lässt sich die
Entwicklungszeit signifikant verkürzen.


    $ docker build . -f Dockerfile-base -t onsei/whisper-base:latest

    ($ docker login)
    $ docker push onsei/whisper-base:latest

    $ docker build . -t onsei/whisper-python:0.3.1.0005
    $ docker push onsei/whisper-python:0.3.1.0005

    # starten ohne GPU-Anbindung
    $ docker run -p 8765:8765 --name whisper-python onsei/whisper-python:0.3.1.0005
    
    # starten mit GPU-Anbindung
    $ docker run --gpus=all -p 8765:8765 --name whisper-python onsei/whisper-phython:0.3.1.0005


## Whisper-CPP

Die Whisper CPP Version ist eine schnellere Variante der Open-AI Whisper Version. Sie wird mit pywhisptercpp
als Python-Bibliothek eingebunden:

    $ pip install pywhispercpp


### Docker

Erzeugen eines Docker-Containers:

    $ docker build . -f Dockerfile-cpp -t onsei/whisper-cpp:0.3.0.0004

    ($ docker login)
    $ docker push onsei/whisper-cpp:0.3.0
    
    $docker run -p 8765:8765 --name whisper onsei/whisper-cpp:0.3.0.0004

mit GPU:

    docker run --gpus=all -p 8765:8765 onsei/whisper-cpp:0.3.0.0004


