FROM onsei/whisper-base:1.0

COPY ./assets/whisper-model.pt /python-docker/assets/whisper-model.pt
COPY ./config /python-docker/config
COPY WhisperConst.py /python-docker
COPY WhisperVersion.py /python-docker
COPY WhisperStreamServer.py /python-docker
WORKDIR /python-docker
EXPOSE 8765
CMD [ "python", "WhisperStreamServer.py"]