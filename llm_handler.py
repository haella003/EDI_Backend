import os
from openai import OpenAI
from dotenv import load_dotenv

# This force-loads the .env file from the current folder
load_dotenv() 

api_key = os.getenv("OPENAI_API_KEY")


"""
# This check will tell us immediately if the key is missing
if not api_key:
    print("CRITICAL ERROR: Your API Key was not found! Check your .env file name.")
else:
    print("API Key loaded successfully. Connecting to OpenAI...")
    
"""

client = OpenAI(api_key=api_key)


def get_edi_response(user_input):
    system_prompt = "You are EDI, an engineering apprentice..." # (Keep your full prompt here)
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    
 # Check if we are actually getting the text
    answer = completion.choices[0].message.content
    return answer

if __name__ == "__main__":
    print("Testing directly from llm_handler...")
    print(get_edi_response("Are you awake?"))