from audio_handler import record_audio, transcribe_audio
from llm_handler import get_edi_response
from speech_handler import speak

def run_edi_loop():
    print("EDI SYSTEM ONLINE")
    
    # keeps the program running forever until user presses Ctrl + C
    while True:
        try:
            print("\nREady for your command...")
            audio_file = record_audio(duration=5)
            
            user_text = transcribe_audio(audio_file)
            
            # skip if nothing was heard
            if not user_text.strip():
                continue
            
            print(f"User: {user_text}")
            
            edi_response = get_edi_response(user_text)
            print(f"EDI: {edi_response}")
            
            speak(edi_response)
            
        except KeyboardInterrupt:
            print("\nShutting down EDI. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            
if __name__ == "__main__":
    run_edi_loop()