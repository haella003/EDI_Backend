from audio_handler import record_audio, transcribe_audio
from llm_handler import get_edi_response
from speech_handler import speak

def run_edi_loop():
    print("\n" + "="*30)
    print("EDI SYSTEM ONLINE")
    print("="*30 + "\n")
    
    # 1. RECORD: capture your voice through the mix
    # you can change duration = 5
    audio_file = record_audio(duration=5)
    
    # 2. TRANSCRIBE: Convert the audio file (.wav) into text
    try:
        user_text = transcribe_audio(audio_file)
        print(f"\nUser: {user_text}")
        
        # 3. THINK: send that text to the LLM
        print("\nEDI is processing data...")
        edi_response = get_edi_response(user_text)
        
        # 4. OUTPUT: Display EDI's technical answer
        print(f"EDI SYSTEM RESPONSE:\n{edi_response}")
        speak(edi_response)
        
        """
        print("\n" + "-"*30)
        print(f"EDI SYSTEM RESPONSE:\n{edi_response}")
        print("-"*30 + "\n")
        """
        
    except Exception as e:
        print(f"System Error: {e}")
        
if __name__ == "__main__":
    run_edi_loop()