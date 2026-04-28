import os

# Your current settings
MODEL_PATH = "/Users/ellapaulahaechler/Desktop/EDI_Backend/piper/en_US-amy-medium.onnx"
test_text = "Attention! EDI has found a lost data packet about education. How exciting!"

full_command = (
    f'echo "{test_text}" | '
    f'python3 -m piper --model {MODEL_PATH} --output_raw | '
    f'ffmpeg -y -f s16le -ar 22050 -ac 1 -i - '
    f'-af "asetrate=22050*1.2, atempo=0.9, vibrato=f=4:d=0.5" ' 
    f'output_test.wav && afplay output_test.wav'
)

os.system(full_command)