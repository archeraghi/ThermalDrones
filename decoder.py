import os
import matplotlib.image as mpimg
import numpy as np

def read_frames_and_decode_binary(folder_path):
    # List all files in the folder and sort them by frame number
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')],
                   key=lambda x: int(x.split('_')[1].split('.')[0]))
    
    binary_string = ''
    
    for filename in files:
        # Load image
        img_path = os.path.join(folder_path, filename)
        img = mpimg.imread(img_path)
        
        # Check the predominant color to determine '1' or '0'
        if np.all(img[:, :, 0] == 1):  # Red channel is full everywhere
            binary_string += '1'
        else:
            binary_string += '0'
    
    return binary_string_to_text(binary_string)

def binary_string_to_text(binary_str):
    # Split the binary string into 8-bit chunks and convert to text
    n = 8
    bytes = [binary_str[i:i+n] for i in range(0, len(binary_str), n)]
    characters = [chr(int(b, 2)) for b in bytes if len(b) == 8]
    return ''.join(characters)

# Define the folder where the frames are saved
frames_folder = 'frames'

# Decode the binary sequence to text
decoded_text = read_frames_and_decode_binary(frames_folder)
print("Decoded text from frames:", decoded_text)

