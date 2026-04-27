import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
# OLD: client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# NEW: local Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",  
    api_key="ollama",                     
)

# EDI's short-term memory
chat_history = []

with open("knowledge.json", "r") as file:
    knowledge_base = json.load(file)
    
def get_relevant_knowledge(user_input):
    
    text = user_input.lower()
    
    for category_name, package_data in knowledge_base.items():
        if category_name == "default":
            continue
        for keyword in package_data["keywords"]:
            if keyword in text:
                print(f"Found relevant knowledge for category '{category_name}')")
                return package_data["info"]
            
    return knowledge_base["default"]["info"]

def load_persona(filename="persona.txt"):
    path = os.path.join("persona", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_edi_response(user_input):
    global chat_history # uses and updates the global chat history list
    
    # calls library to get the most relevant knowledge package based on the user input
    current_package = get_relevant_knowledge(user_input)
    base_instructions = load_persona("persona.txt")
    
    system_prompt = f"""
    {base_instructions}
    
    CURRENT CONTEXT/KNOWLEDGE:
    {current_package}"""
    
    # user input to chat history
    chat_history.append({"role": "user", "content": user_input})
    
    # sliding window: keeps only the last 10 messages (5 user + 5 assistant)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
        
    messages_to_send = [{"role": "system", "content": system_prompt}] + chat_history
    
    try:
        completion = client.chat.completions.create(
            model="gemma3:4b", # change
            messages=messages_to_send,
            max_tokens=150
        )
        
        response_text = completion.choices[0].message.content
        
        # Print it to verify it is just a clean string now
        # print(f"DEBUG: Cleaned Text is: {response_text}")
        
        chat_history.append({"role": "assistant", "content": response_text})
        
        # Return the clean string back to main.py
        return response_text
        
    except Exception as e:
        if chat_history and chat_history[-1]["role"] == "user":
            chat_history.pop()

        return f"[SORRY] | Brain Error: {str(e)}"
    
def reset_memory():
    """Wipes EDI's short-term memory clean for the next session."""
    global chat_history
    chat_history = []
    print("API Triggered: EDI'smemory has been completely wiped.")