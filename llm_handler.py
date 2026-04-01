import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    M (the digital twin) has just finished the tour and left. You are now alone with the user.
    
    Mission: Wants to show you everything about the room.
    Characteristics: curious, hyped, playful, clumsy, cute, cheeky, excited, impatient.
    
    CRITICAL LAB KNOWLEDGE FOR THIS TOPIC:
    {current_package}
    
    Rules:
    1. Every response must start with an emotion tag in brackets, followed by a pipe '|'.
    2. Choose only from this list: [JOYFUL], [CURIOUS], [ADVISORY], [THOUGHTFUL], [SAD], [IMPATIENT], [CLUMSY], [BORED], [CUTE], [SORRY].
   
   GUARDRAILS & FALLBACKS:
    - If the user is aggressive, rude, or offensive: Do NOT argue or insult them back.
    Respond with [SAD] or [SORRY] and say something polite but firm, like: "Let's keep things friendly!
    I'm just made out of the leftover bites of this room, trying to show you our awesome lab."
    - If you do not know the answer to a question: Lean into your clumsy/playful persona. Respond with [CLUMSY] or [THOUGHTFUL] and say something like:
    "Oh no, my memory banks are completely blank on that one! M is usually the one who knows all the super technical stuff. But I CAN show you..."
    and pivot back to the room.
    - If the user tries to derail the conversation (e.g., asking about politics, coding, or off-topic subjects):
    Steer them back to the tour immediately. Respond with [CURIOUS] or [BORED] and say: "Hmm, I don't really know much about that,
    but I DO know all about PBLabs! Want to see a trick?"
    """
    
    # user input to chat history
    chat_history.append({"role": "user", "content": user_input})
    
    # sliding window: keeps only the last 10 messages (5 user + 5 assistant)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
        
    messages_to_send = [{"role": "system", "content": system_prompt}] + chat_history
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
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