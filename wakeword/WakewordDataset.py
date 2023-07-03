#!/usr/bin/env python


from datasets import load_dataset, Dataset, DatasetDict, Audio


# Array mit allen Audio-Dateinamen

trainAudioList = [
    "./audio/aida-kws-1.wav",
    "./audio/aida-kws-2.wav",
    "./audio/aida-kws-4.wav",
    "./audio/aida-kws-5.wav",
    "./audio/aida-kws-6.wav",
    "./audio/aida-kws-7.wav",
    "./audio/aida-kws-9.wav",
    "./audio/aida-kws-10.wav",
    "./audio/aida-kws-11.wav",
    "./audio/aida-kws-12.wav",
    "./audio/aida-kws-14.wav",
    "./audio/aida-kws-15.wav",
    "./audio/aida-kws-16.wav",
    "./audio/aida-kws-17.wav",
    "./audio/aida-kws-18.wav",
    "./audio/aida-kws-20.wav",
    "./audio/aida-kws-21.wav",
    "./audio/aida-kws-22.wav",
    "./audio/aida-kws-24.wav",
    "./audio/aida-kws-25.wav"
]

testAudioList = [
    "./audio/aida-kws-3.wav",
    "./audio/aida-kws-8.wav",
    "./audio/aida-kws-13.wav",
    "./audio/aida-kws-19.wav",
    "./audio/aida-kws-23.wav"
]

trainTextList = [
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella"
]

testTextList = [
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella",
    "Ahoi Stella"
]

# Erzeugen eines eigenen Wakeword-Datesets zum Training von Whisper

print( "Alle Audio-Dateien werden eingelesen...")
audioTrainDataset = Dataset.from_dict({"sentence": trainTextList, "audio": trainAudioList}).cast_column("audio", Audio(sampling_rate=16000))
audioTestDataset = Dataset.from_dict({"sentence": testTextList, "audio": testAudioList}).cast_column("audio", Audio(sampling_rate=16000))

print( "Erster Train Datenset: ", audioTrainDataset[0])
print( "Erster Test Datenset: ", audioTestDataset[0])
print( "Alle Audio-Dateien sind eingelesen")
