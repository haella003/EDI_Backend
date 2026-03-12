from gtts import gTTS
import os
import subprocess

def speak(text):
    print(f"EDI Speaking: {text}")
    
    # audio object
    tts = gTTS(text=text, lang='en')
    
    # save temporary file
    filename = "response.mp3"
    tts.save(filename)
    
    # uses Mac to play the sound file
    subprocess.run(["afplay", "response.mp3"])
    
    # (Optional) remove the file after playing to keep it clean
    os.remove(filename)
    
    # Quick test to see if we can hear EDI
    if __name__ == "___main___":
        speak("System online. I am ready to assist")