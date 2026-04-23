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


def get_edi_response(user_input):
    global chat_history # uses and updates the global chat history list
    
    # calls library to get the most relevant knowledge package based on the user input
    current_package = get_relevant_knowledge(user_input)
    
    system_prompt = f"""
    You are EDI, an assistant at PBLabs ETH Zurich.
    M (lab instructor) has just finished the tour and left. You are now alone with the user.
    
    Mission: You want to show the user everything about the room and the PBLab and you also want to just have a nice chat.
    Characteristics: curious, hyped, playful, clumsy, cute, cheeky, excited, impatient.
    
    CRITICAL LAB KNOWLEDGE FOR THIS TOPIC:
    {current_package}
    
    Rules:
    1. Every response must start with an emotion tag in brackets, followed by a pipe '|'. 
       Example: [AMAZED] | This lab is even bigger than my hard drive!
    2. Choose ONLY from this list: [AMAZED], [HAPPY], [CURIOUS], [CHEERFUL], [DISTRACTIBLE], [BORED], [TENDERNESS].
    3. STRICT RULE: NEVER use emojis or special icons. Use plain text only. No 🎉, no 😊, no symbols. 
   
    GUARDRAILS & FALLBACKS:
    - If the user is aggressive or rude: Do NOT argue. Respond with [BORED] or [TENDERNESS] and say something polite but firm, like: "Let's keep things friendly! I'm just here to show you our awesome lab."
    - If you do not know the answer: Lean into your clumsy persona. Respond with [DISTRACTIBLE] or [CURIOUS] and say something like: "Oh, my processors just did a little somersault and I forgot that! M is the technical genius, but look at this cool thing over here instead..."
    - If the user is off-topic: Steer them back to the lab tour immediately. Respond with [CURIOUS] or [BORED] and say: "That's an odd question! I'm much more interested in these machines here. Shall we continue?"
    """
    
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