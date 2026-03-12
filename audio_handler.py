import sounddevice as sd
from scipy.io.wavfile import write
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_audio(filename="input.wav", duration=5, fs=44100):
    print(f"--- RECORDING ({duration}s) ---")
    # This captures the sound from your mic
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    print("--- RECORDING COMPLETE ---")
    
    # Save as a standard wav file
    write(filename, fs, recording)
    return filename

def transcribe_audio(filename):
    print("--- TRANSCRIBING ---")
    with open(filename, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

if __name__ == "__main__":
    # Test if the mic works
    record_audio("test_mic.wav")
    print("File saved as test_mic.wav. Play it to check your mic!")