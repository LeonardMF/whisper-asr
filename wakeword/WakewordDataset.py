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
    "./audio/aida-kws-25.wav",
    "./audio/aida-kws-26.wav",
    "./audio/aida-kws-27.wav",
    "./audio/aida-kws-28.wav",
    "./audio/aida-kws-30.wav",
    "./audio/aida-kws-31.wav",
    "./audio/aida-kws-32.wav",
    "./audio/aida-kws-33.wav",
    "./audio/aida-kws-34.wav",
    "./audio/aida-kws-35.wav",
    "./audio/aida-kws-36.wav",
    "./audio/aida-kws-38.wav",
    "./audio/aida-kws-39.wav",
    "./audio/aida-kws-40.wav",
    "./audio/aida-kws-42.wav",
    "./audio/aida-kws-43.wav",
    "./audio/aida-kws-44.wav",
    "./audio/aida-kws-45.wav",
    "./audio/aida-kws-46.wav",
    "./audio/aida-kws-47.wav",
    "./audio/aida-kws-49.wav",
    "./audio/aida-kws-50.wav",
    "./audio/aida-kws-51.wav",
    "./audio/aida-kws-52.wav",
    "./audio/aida-kws-54.wav"
]

testAudioList = [
    "./audio/aida-kws-3.wav",
    "./audio/aida-kws-8.wav",
    "./audio/aida-kws-13.wav",
    "./audio/aida-kws-19.wav",
    "./audio/aida-kws-23.wav",
    "./audio/aida-kws-29.wav",
    "./audio/aida-kws-37.wav",
    "./audio/aida-kws-41.wav",
    "./audio/aida-kws-48.wav",
    "./audio/aida-kws-53.wav"
]


# Erzeugen der Textlisten

trainTextList = []
for index in trainAudioList:
    trainTextList.append("Ahoi Stella")

testTextList = []
for index in testAudioList:
    testTextList.append("Ahoi Stella")


# Erzeugen eines eigenen Wakeword-Datesets zum Training von Whisper

print( "Alle Audio-Dateien werden eingelesen...")
audioTrainDataset = Dataset.from_dict({"sentence": trainTextList, "audio": trainAudioList}).cast_column("audio", Audio(sampling_rate=16000))
audioTestDataset = Dataset.from_dict({"sentence": testTextList, "audio": testAudioList}).cast_column("audio", Audio(sampling_rate=16000))

print( "Alle Audio-Dateien sind eingelesen")
