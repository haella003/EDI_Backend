import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2

load_dotenv() 

client = OpenAI(
    base_url="http://localhost:11434/v1",  
    api_key="ollama",                     
)

chat_history = []

# knowledge base
def get_pdf_content():
    """Reads all text from any PDF files in the knowledge_vault folder."""
    pdf_text = ""
    vault_path = "knowledge_vault"
    
    if not os.path.exists(vault_path):
        return ""

    for filename in os.listdir(vault_path):
        if filename.endswith(".pdf"):
            try:
                with open(os.path.join(vault_path, filename), "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        content = page.extract_text()
                        if content:
                            pdf_text += content + "\n"
            except Exception as e:
                print(f"Error reading PDF {filename}: {e}")
    return pdf_text

def get_relevant_knowledge(user_input):
    text = user_input.lower()
    combined_info = ""
    
    # Load the JSON
    json_path = os.path.join("knowledge_vault", "knowledge.json")
    try:
        with open(json_path, "r") as file:
            knowledge_base = json.load(file)
    except FileNotFoundError:
        return "No specific lab knowledge found."

    # Check for keyword matches in the JSON and combine relevant info
    found_keywords = []
    for category_name, package_data in knowledge_base.items():
        if category_name == "default":
            continue
        for keyword in package_data["keywords"]:
            if keyword in text:
                found_keywords.append(category_name)
                combined_info += f"FACT ({category_name}): {package_data['info']}\n"
    
    if found_keywords:
        print(f"Combined JSON matches: {', '.join(found_keywords)}")
            
    # Add default info at the end
    default_info = knowledge_base.get("default", {}).get("info", "")
    combined_info = f"GENERAL LAB RULES: {default_info}\n\n" + combined_info
    
    # Add PDF content
    pdf_info = get_pdf_content()
    if pdf_info:
        combined_info += f"\nTECHNICAL MANUAL DETAILS:\n{pdf_info[:2000]}" # limit to first 2000 chars to avoid overwhelming the prompt
        
    return combined_info
        
# persona loading
def load_persona(filename="EDI_RZ_1.txt"):
    path = os.path.join("personas", filename)
    if not os.path.exists(path):
        return "You are a helpful assistant."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
# main response logic
def get_edi_response(user_input):
    global chat_history # uses and updates the global chat history list
    
    # calls library to get the most relevant knowledge package based on the user input
    current_package = get_relevant_knowledge(user_input)
    base_instructions = load_persona("EDI_RZ_1.txt")
    
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