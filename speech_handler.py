import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speak(text):
    # This creates a solid path to your project folder
    speech_file_path = Path.cwd() / "temp_speech.mp3"
    
    try:
        print(f" EDI is thinking of how to say: '{text[:20]}...'")
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )

        # 1. Save the file
        response.stream_to_file(speech_file_path)

        # 2. Play the file using the absolute path
        # The quotes around {speech_file_path} help if your folder names have spaces
        os.system(f'afplay "{speech_file_path}"')

        # 3. Clean up
        if speech_file_path.exists():
            os.remove(speech_file_path)
        
    except Exception as e:
        print(f" Voice Error: {e}")
        
if __name__ == "__main__":
    speak("Hello PBLabs! I am EDI, and I am hyped to be here at ETH Zurich!")
    