import time
import click
import requests

@click.command()
@click.option(
    "--audio_file_name",
    default="deutsch",
    type=str,
    help="Name of the audio file in audio folder",
)
@click.option(
    "--url",
    default="http://localhost",
    type=str,
    help="url of the server",
)
@click.option(
    "--port",
    default="5001",
    type=str,
    help="port of the server",
)
def main(audio_file_name: str, url: str, port: str):
    
    url = f"{url}:{port}/whisper"
    
    audio_file = open(f"./audio/{audio_file_name}.mp3", "rb")
    request_start_time = time.time()
    response = requests.post(url, files={audio_file_name: audio_file})
    response_time = time.time()
    print(f"Request duration: {response_time - request_start_time}")
    for k,v in response.json().items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()