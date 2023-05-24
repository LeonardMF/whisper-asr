FROM python:3.10-slim

WORKDIR /python-docker

COPY requirements-docker.txt requirements.txt
RUN apt-get update && apt-get install git -y
RUN pip3 install -r requirements.txt
RUN pip3 install "git+https://github.com/openai/whisper.git" 
RUN apt-get install -y ffmpeg

COPY server.py server.py

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--app", "server", "run", "--host=0.0.0.0"]