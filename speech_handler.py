import os
import re

def speak(text):
    try:
        # 1. clean text e.g. remove [JOYFUL] |
        clean_text = re.sub(r"\[.*?\]\s*\|\s*", "", text)
        
        # 2. delete Emojis and non-ASCII characters
        clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)
        
        # 3. remove exclamation and quotation marks
        clean_text = clean_text.replace('"', '').replace("'", "")

        # speak only if there is text left after filtering
        if clean_text.strip():
            print(f"--- EDI SPEAKING (No Emojis): {clean_text[:30]}... ---")
            # the Mac command 'say'
            os.system(f'say -v Samantha "{clean_text}"')
    
    except Exception as e:
        print(f" Voice Error: {e}")
            
if __name__ == "__main__":
    # Test with emotion tag
    speak("[JOYFUL] | I am EDI, running locally on your hardware. Hello PBLabs, I am hyped to be here at ETH Zurich!")