import re
import llm_handler # Import this directly to talk to the AI brain

def run_chat_test():
    print("--- EDI OFFLINE CHAT MODE ---")
    print("Type your message to test logic. Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("\nDisconnecting from EDI... Goodbye.")
                break
                
            if not user_input:
                continue
            
            # 1. Get the raw response from the LLM
            raw_response = llm_handler.get_edi_response(user_input)
            
            # 2. Parse the pipe
            if "|" in raw_response:
                # We use [-1] to always get the last part (the message)
                message = raw_response.split("|")[-1].strip()
            else:
                message = raw_response
                
            # Scrub the brackets []
            clean_message = re.sub(r'\[.*?\]', '', message).strip()
            clean_message = clean_message.replace("|", "").strip()
                
            # 3. Show the result 
            print(f"EDI: {clean_message}")
            
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Closing...")
            break
        except Exception as e:
            print(f"\n[SYSTEM ERROR]: {e}")

if __name__ == "__main__":
    run_chat_test()