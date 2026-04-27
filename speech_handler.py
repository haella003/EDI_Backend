import os
import re
import subprocess

PIPER_PATH = "/Users/ellapaulahaechler/Desktop/EDI_Backend/piper/piper"
MODEL_PATH = "/Users/ellapaulahaechler/Desktop/EDI_Backend/piper/en_US-amy-medium.onnx"

def speak(text):
    try:
        # clean text
        clean_text = re.sub(r"\[.*?\]\s*\|\s*", "", text)
        clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)
        clean_text = clean_text.replace('"', '').replace("'", "")
        clean_text = re.sub(r"\*.*?\*", "", clean_text)

        # speak only if there is text left after filtering
        if not clean_text.strip():
            return
        
        print(f"--- EDI SPEAKING (No Emojis): {clean_text[:40]}... ---")
            
        # Piper generates Audio and sends it to ffmpeg
        # filter description: 
        # asetrate=44100*1.15 -> voice pitch
        # atempo=0.9 -> voice speed
        
        full_command = (
            f'echo "{clean_text}" | '
            f'{PIPER_PATH} --model {MODEL_PATH} --output_raw | '
            f'ffmpeg -y -f s16le -ar 22050 -ac 1 -i - '
            f'-af "asetrate=22050*1.15,atempo=0.9" '
            f'output_edi.wav && afplay output_edi.wav'
        )
        
        os.system(full_command)
    
    except Exception as e:
        print(f" Voice Error: {e}")
            
if __name__ == "__main__":
    # Test with emotion tag
    speak("[JOYFUL] | I am EDI, running locally on your hardware. Hello PBLabs, I am hyped to be here at ETH Zurich!")