import time
import datetime
from audio_handler import record_audio, transcribe_audio
import llm_handler
from logger_handler import save_chat_log
from speech_handler import speak

def run_edi_loop(shared_data):
    print("EDI SYSTEM ONLINE. WAITING FOR SESSION TO START...")
    first_run = True
    session_id = "default"

    while True:
        try:
            # 0. CHECK FOR MEMORY WIPE FROM API
            if shared_data.get("reset_memory"):
                print(f"Main: API triggered memory wipe! Reason: {shared_data.get('end_reason')}")
                llm_handler.reset_memory() # Clear the sliding window
                shared_data["reset_memory"] = False
                first_run = True # Reset this so the next user gets a fresh session ID
                continue # Skip the rest of the loop and wait for the new user
            
            # 1. CHECK THE SHARED WHITEBOARD
            if not shared_data.get("session_active"):
                shared_data["status"] = "idle"
                shared_data["emotion"] = "NEUTRAL"
                first_run = True
                time.sleep(1)
                continue
            
            # 2. GREETING LOGIC
            if shared_data.get("trigger_first_speech"):
                if first_run:
                    session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    first_run = False
                
                shared_data["status"] = "thinking"
                print(f"Main: API triggered first speech! Mode: {shared_data.get('start_mode')}")
                
                # Tell the LLM how to greet the user based on the API command
                if shared_data.get("start_mode") == "m_handoff":
                    intro_prompt = "M just finished the tour and left. Introduce yourself to the user playfully!"
                else:
                    intro_prompt = "The user skipped M's intro. Greet them directly and energetically!"
                
                raw_response = llm_handler.get_edi_response(intro_prompt)
                
                # Parse emotion (Using your awesome code!)
                if "|" in raw_response:
                    parts = raw_response.split("|", 1)
                    shared_data["emotion"] = parts[0].replace("[", "").replace("]", "").strip()
                    shared_data["message"] = parts[1].strip()
                else:
                    shared_data["emotion"] = "NEUTRAL"
                    shared_data["message"] = raw_response
                    
                shared_data["status"] = "speaking"
                print(f"EDI: {shared_data['message']}")
                save_chat_log("EDI", shared_data["message"], shared_data["emotion"], session_id)
                speak(shared_data["message"])
                
                # Turn off the flag so he doesn't repeat the intro forever!
                shared_data["trigger_first_speech"] = False
                continue # Jump back to the start of the loop to enter listening phase 
            
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