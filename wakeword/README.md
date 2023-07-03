# Wakeword-Training mit Whisper

Hier wird ein experimenteller Code zum Finetuning Training von Whisper für ein Wakeword erstellt.
Damit soll die Erkennungsgenauigkeit eines Wakewords verbessert werden. 

Zunächst werden Experimente mit Mozillas Common-Voice Datensatz durchgeführt, um das Prinzip des
Finetunings von Whisper zu verstehen. 

Danach werden die eigenen Audio-Dateien für das Wakeword zum Training verwendet.

Alternativen Code zum Training gibt es in:

    * fine_tune_whisper.py - Beispiel aus dem Tutorial
    * run_speech_recognition_seq2seq.py - von Huggingface
    * run_speech_recognition_whisper.py - angepasste Version von Huggingface
    * audiowhisper_train_v00001.py - eigene Version

Das eigene Trainingsprogramm ist in:

    * WhisperWakewordTrain.py - Training der Audiodaten
    * WakewordDataset.py - Eigenes Audio-Datenset erstellen