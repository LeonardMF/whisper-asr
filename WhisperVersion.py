# Konstanten fuer die Whisper-Version


# extern

import os
import json


# Laden der Konfiguration aus einer JSON-Datei

def _loadConfig( aConfigFileName: str):
    try:
        # Laden der Konfigurationsdatei des Geraetes

        jsonFile = open(aConfigFileName)
        if jsonFile is not None:
            return json.load(jsonFile)
        # logger.error("_loadConfig: Keine Datei vorhanden")
        return None
    except Exception as aException:
        # logger.exception("_loadConfig: " + str(aException))
        return None


# absoluten Dateinamen erzeugen

filePath = os.getcwd() + "/config/whisper-version.json"

# JSON-Datei einlesen
whisperVersion = _loadConfig( filePath )
if whisperVersion is not None:
    WHISPER_VERSION = whisperVersion.get("WHISPER_VERSION_NUMBER")
    WHISPER_DATE = whisperVersion.get("WHISPER_VERSION_DATE")
    WHISPER_BUILD = whisperVersion.get("WHISPER_VERSION_BUILD")
else:
    WHISPER_VERSION = "0.X.0"
    WHISPER_DATE = "XX.10.2022"
    WHISPER_BUILD = "XXXX"
