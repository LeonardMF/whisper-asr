from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import whisper
# import torch

# Check if NVIDIA GPU is available
# torch.cuda.is_available()
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DEVICE = "cpu"
# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)
print("app: ", app)

@app.route("/")
def hello():
    return "Hello Whisper!"

@app.route('/whisper', methods=['POST'])
def handler():
    print("request: ", request.files)
    if not request.files:
        # If the user didn't submit any files, return a 400 (Bad Request) error.
        abort(400)

    # For each file, let's store the results in a list of dictionaries.
    result = {}

    # Loop over every file that the user submitted.
    for filename, handle in request.files.items():
        # Create a temporary file.
        # The location of the temporary file is available in `temp.name`.
        temp = NamedTemporaryFile()
        # Write the user's uploaded file to the temporary file.
        # The file will get deleted when it drops out of scope.
        handle.save(temp)
        
        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(temp.name)
        audio = whisper.pad_or_trim(audio)
        
        # Let's get the transcript of the temporary file.
        transcribe_result = model.transcribe(audio)
        
        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
    
        # detect the spoken language
        _, probs = model.detect_language(mel)
        detected_language = max(probs, key=probs.get)
        
        # Now we can store the result object for this file.
        result['audio_file_name'] = filename
        result['detected_language'] = detected_language
        result['transcription'] = transcribe_result['text']
        
        # Translate if the language is not English
        if detected_language != "en":
            translate_result = model.transcribe(audio, task = 'translate', fp16=False)
            result['translation'] = translate_result['text']

    # This will be automatically converted to JSON.
    return result