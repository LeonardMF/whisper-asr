FROM onsei/whisper-base

WORKDIR /python-docker

COPY whisper_stream_server.py whisper_stream_server.py

EXPOSE 8765

CMD [ "python", "whisper_stream_server.py"]