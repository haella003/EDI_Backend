from llm_handler import get_edi_response

print("--- TEST START ---")

try:
    print("Talking to EDI... please wait...")
    result = get_edi_response("EDI, explain your current status.")
    print("EDI says:")
    print(result)
except Exception as e:
    print(f"An error occurred: {e}")

print("--- TEST END ---")