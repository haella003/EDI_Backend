import time
import datetime
from audio_handler import record_audio, transcribe_audio
from llm_handler import get_edi_response
from logger_handler import save_chat_log
from speech_handler import speak

def run_edi_loop(shared_data):
    print("EDI SYSTEM ONLINE. WAITING FOR SESSION TO START...")
    first_run = True
    session_id = "default"

    while True:
        try:
            # 1. CHECK THE SHARED WHITEBOARD
            if not shared_data.get("session_active"):
                shared_data["status"] = "idle"
                shared_data["emotion"] = "NEUTRAL"
                first_run = True
                time.sleep(1)
                continue
            
            # 2. GREETING LOGIC
            if first_run:
                session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                shared_data["status"] = "speaking"
                greeting = "Finally! M is gone. I'm Eddie. What should we explore first?"
                print(f"EDI: {greeting}")
                
                save_chat_log("EDI", greeting, "JOYFUL", session_id) # Logger for greeting
                speak(greeting)
                
                first_run = False 
            
            # 3. LISTENING PHASE
            shared_data["status"] = "listening"
            print("\nListening...")
            
            audio_file = record_audio()
            user_text = transcribe_audio(audio_file)
            
            # guard against empty input
            if not user_text or not user_text.strip():
                continue
            
            print(f"User: {user_text}")
            save_chat_log("User", user_text, "NEUTRAL", session_id)  # Logger for user input
            
            # 4. THINKING PHASE
            shared_data["status"] = "thinking"
            raw_response = get_edi_response(user_text)
            print(f"EDI (raw): {raw_response}")
            
            if "|" in raw_response:
                parts = raw_response.split("|", 1)
                shared_data["emotion"] = parts[0].replace("[", "").replace("]", "").strip()
                shared_data["message"] = parts[1].strip()
            else:
                shared_data["emotion"] = "NEUTRAL"
                shared_data["message"] = raw_response
            
            # 5. SPEAKING PHASE
            shared_data["status"] = "speaking"
            save_chat_log("EDI", shared_data["message"], shared_data["emotion"], session_id)  # Logger for EDI reponse
            speak(shared_data["message"])
            
        except KeyboardInterrupt:
            shared_data["status"] = "offline"
            print("\nShutting down EDI. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            shared_data["status"] = "error"
            time.sleep(2)