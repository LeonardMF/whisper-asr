# Whisper-ASR Server

Der Whisper-ASR Server dient der Kapselung der Whisper-ASR und der Anbindung des ASR-Dienstes über eine Websocket.
Es gibt zwei unterschiedliche Versionen der Whisper-ASR. Einmal die PyTorch Version mit OpenAI-Whisper als
Python- Implementierung. Zum anderen eine reine C++ Implementierung ohne Python.


## Whisper-ASR (Python)

Die Whisper-Python Version ist die offizielle Version von Open-AI mit deren Python-API und einem Websocket-Server.

### Docker

Fuer diese Version von Whisper werden zwei Docker-Container erzeugt. Der Whisper-Base Container enthält alle
Python-Installationen für Whisper selbst. Dieser Container verwendet den öffentliche  PyTorch/PyToch Contaiher.
Der Whisper-Asr Container enthaelt den Whisper-Asr Server Code. Damit lässt sich die Entwicklungszeit signifikant
verkürzen, weil die Ladezeiten der Container kürzer werden.


    $ docker build . -f Dockerfile-base -t onsei/whisper-base:1.0

    ($ docker login)
    $ docker push onsei/whisper-base:1.0

    $ docker build . -t onsei/whisper-asr:0.3.1.0005
    $ docker push onsei/whisper-asr:0.3.1.0005

    # starten ohne GPU-Anbindung
    $ docker run -p 8765:8765 --name whisper-asr onsei/whisper-asr:0.3.1.0005
    
    # starten mit GPU-Anbindung
    $ docker run --gpus=all -p 8765:8765 --name whisper-asr onsei/whisper-asr:0.3.1.0005


## Whisper-ASR (C++)

Die Whisper CPP Version ist eine schnellere Variante der Open-AI Whisper Version. 
Für einen ersten Python-Prototyp des Whisper-ASR Servers mit C++ wird pywhisptercpp
als Python-Bibliothek eingebunden:

    $ pip install pywhispercpp

Später gibt es eine reine C++ Version des Whisper-ASR Servers mit Websockets. Diese wird
die finale Version für eine zukünftige Whisper-ASR als Cloud Server Lösung.


### Docker

Erzeugen eines Docker-Containers:

    $ docker build . -f Dockerfile-cpp -t onsei/whisper-cpp:0.3.0.0004

    ($ docker login)
    $ docker push onsei/whisper-cpp:0.3.0
    
    $docker run -p 8765:8765 --name whisper onsei/whisper-cpp:0.3.0.0004

mit GPU:

    docker run --gpus=all -p 8765:8765 onsei/whisper-cpp:0.3.0.0004


