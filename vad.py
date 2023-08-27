import time
import sounddevice as sd
import numpy as np
import wave
import webrtcvad

# EOS
class MyEOS():
    def __init__(self):
        self.start_of_speech_flag = False
        self.start_time = time.time()
        
    def detect_end_of_speech(self, audio_data):
        audio_data_mean = np.mean(audio_data)
        
        print(audio_data_mean)
        
        if np.mean(audio_data) > 10:
            self.start_of_speech_flag = True 
            self.start_time = time.time()
            
        if self.start_of_speech_flag and time.time() - self.start_time >= 0.5:
            return True
        
        return False
    
# VAD
class VadAnalyzer:
    def __init__(self, 
                 samplerate = 48000 # 16000, 32000 or 48000
                ):
        self.samplerate = samplerate
        self.vad = webrtcvad.Vad()
        self.vad.set_mode( 3 )
        self.startTimeout =  5.0 # seconds since start audio stream
        self.endTimeout  =  0.2 # seconds since end of voice detected
        self.voiceCounter = 0
        self.frameTime = time.time()
    
    def detect_end_of_speech(self, audio):
        # VAD analysis
        frame_duration = 10  # ms
        frame_len = int(self.samplerate * 10 / 500)
        frame_list = [audio[i:i + frame_len] for i in range(0, len(audio), frame_len)]
        
        for frame in frame_list:
            
            length = frame_len - len( frame )
            
            if length > 0:
                frame = b'\x00\x00' * int(self.samplerate * frame_duration / 1000)
                
            voice_flag = self.vad.is_speech(frame, self.samplerate)
            
            if voice_flag:
                self.voiceCounter += 1
                # Set timeout for end of speech to 200ms
                if self.voiceCounter == 20:
                    print(f"StartOfSpeech: voiceCounter={self.voiceCounter}")
                    self.startTimeout = self.endTimeout
                self.frameTime = time.time()
            else:
                self.voiceCounter += 0
                currentTime = time.time()
                if currentTime - self.frameTime > self.startTimeout:
                    return True
        
        return False

if __name__ == "__main__":       
    samplerate = 48000 # 16000, 32000 or 48000
    channels = 1

    vad_analyzer = VadAnalyzer(samplerate)
    my_eos = MyEOS()

    # Configure sounddevice input stream
    stream = sd.InputStream(
        channels=channels,
        samplerate=samplerate,
        dtype=np.int16,
    )

    # Start recording audio
    stream.start()

    waveFile = wave.open("vad_test.wav", "wb")
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(2)  # 2 bytes per sample
    waveFile.setframerate(samplerate)

    endOfSpeechFlag = False

    while True:
        # Read audio data from input stream
        audio_data, _ = stream.read(1024)
        # endOfSpeechFlag = my_eos.detect_end_of_speech(audio_data)
        audio = audio_data.tobytes()
        endOfSpeechFlag = vad_analyzer.detect_end_of_speech(audio)
        
        if not endOfSpeechFlag:
            waveFile.writeframes(audio)

        if endOfSpeechFlag:
            print("END OF SPEECH DETECTED!!!")
            break
            
    print("END!!!")    
