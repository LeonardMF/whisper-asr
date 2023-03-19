import whisper
import click

@click.command()
@click.option(
    "--audio_file_name",
    default="deutsch",
    type=str,
    help="Name of the audio file in audio folder",
)
def main(audio_file_name: str):
    model = whisper.load_model("base")

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(f"./audio/{audio_file_name}.mp3")
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(f"Detected text: {result.text}")

    # run the transcribe with translation
    german_to_english = model.transcribe(audio, task = 'translate', fp16=False)

    # print result
    print(f"Translated transcribt:{german_to_english['text']}")
    
if __name__ == "__main__":
    main()