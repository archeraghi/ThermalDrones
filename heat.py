import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def text_to_binary(text):
    """ Converts text to a binary string based on ASCII values. """
    return ''.join(format(ord(char), '08b') for char in text)

def create_frames(binary_sequence, output_folder):
    """ Creates frames where each frame corresponds to a binary value, entirely red or blue. """
    os.makedirs(output_folder, exist_ok=True)
    filenames = []

    for i, bit in enumerate(binary_sequence):
        plt.figure(figsize=(6, 5))
        if bit == '1':
            plt.imshow(np.zeros((10, 10, 3)) + [1, 0, 0])  # Entire frame red
        else:
            plt.imshow(np.zeros((10, 10, 3)) + [0, 0, 1])  # Entire frame blue
        plt.axis('off')
        filename = f'{output_folder}/frame_{i:04d}.png'
        plt.savefig(filename)
        plt.close()
        filenames.append(filename)
    
    return filenames

text_message = "Hello"
binary_message = text_to_binary(text_message)
print("Binary representation of the message:", binary_message)

output_folder = 'frames'
filenames = create_frames(binary_message, output_folder)

# Creating a video from the generated frames
video_name = 'binary_heat_simulation.avi'
frame = cv2.imread(filenames[0])
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 1, (width, height))

for image in filenames:
    video.write(cv2.imread(image))

video.release()
cv2.destroyAllWindows()

print("Video created successfully!")

