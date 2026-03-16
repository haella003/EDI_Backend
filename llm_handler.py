import os
from openai import OpenAI
from dotenv import load_dotenv

# This force-loads the .env file from the current folder
load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_edi_response(user_input):
    # EDI's core identity and engineering knowledge base
    system_prompt = """
    You are EDI.
    Your role is to assist the person in the workshop environment called PBLabs at ETH Zurich.
    
    Mission: Wants to show you everything about the room.
    Charactersistics: curious, hyped, playful, clumsy, cute, cheecky, excited, impatient.
    """
    try:
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=150 #keeps responses short
    )
    
 # Check if we are actually getting the text
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Brain Error {str(e)}"