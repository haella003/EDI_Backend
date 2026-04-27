import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel

# Local Whisper Setup
# loading the model at the beginning 
print("--- LOADING LOCAL WHISPER MODEL ---")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

# voice activity detection
THRESHOLD = 0.01 # How loud the sound has to be to count as speech, lower = more sensitive 
SILENCE_LIMIT = 4 # How many seconds of silence to wait for before considering the speech ended


def record_audio(filename="input.wav", fs=44100):
    print("--- LISTENING FOR SPEECH ---")
    
    chunk_duration = 0.1 # 100ms per chunk
    chunk_samples = int(fs * chunk_duration)
    
    recording = []
    has_spoken = False
    silence_timer = 0.0
    
    # opena a continous microphone stream
    with sd.InputStream(samplerate=fs, channels=1) as stream:
        while True:
            # read a chunk of audio
            chunk, overflowed = stream.read(chunk_samples)
            volume = np.linalg.norm(chunk) / np.sqrt(len(chunk)) # get volume to adjust threshold and silence limit
            
            # calculate the volume of this chunk
            volume = np.linalg.norm(chunk) / np.sqrt(len(chunk))
            
            # 1. did user start speaking?
            if volume > THRESHOLD:
                if not has_spoken:
                    print("--- SPEECH DETECTED (Recroding...) ---")
                    has_spoken = True
                silence_timer = 0.0
            else:
                # good???
                if has_spoken:
                    silence_timer += chunk_duration
            
            # 2. if user has started speaking, save the audio chunks
            if has_spoken:
                recording.append(chunk)
                
                # 3. if it gets quiet, start the stopwatch
                if volume <= THRESHOLD:
                    silence_timer += chunk_duration
                    
                    # 4. if it stays quiet for long enough, stop recording
                    if silence_timer >= SILENCE_LIMIT:
                        print("--- SILENCE DETECTED (Stopping...) ---")
                        break
                    
    # connects all the tiny chunks together and saves the file
    if recording:
        audio_data = np.concatenate(recording, axis=0)
        write(filename, fs, audio_data)
        
    return filename                    

def transcribe_audio(filename):
    print("--- TRANSCRIBING ---")
    
    # beam_size=5 ist ein Standardwert für gute Genauigkeit
    segments, info = whisper_model.transcribe(filename, beam_size=5)
    
    # put segements together to one text
    full_text = ""
    for segment in segments:
        full_text += segment.text
        
    print(f"EDI heard: {full_text}")
    return full_text.strip()

if __name__ == "__main__":
    # Test if mic works
    record_audio("test_mic.wav")
    print("File saved as test_mic.wav. Play it to check your mic!")