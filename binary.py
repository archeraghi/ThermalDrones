import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import cv2
import argparse

def text_to_binary(text):
    """ Converts text to a binary string based on ASCII values. """
    return ''.join(format(ord(char), '08b') for char in text)

def create_color_frames_from_binary(binary_sequence, output_folder):
    """ Creates color frames based on the binary sequence where '1' is red and '0' is blue. """
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # Remove the folder and all its contents
    os.makedirs(output_folder)  # Create the folder again
    
    for i, bit in enumerate(binary_sequence):
        plt.figure(figsize=(6, 5))
        if bit == '1':
            plt.imshow(np.zeros((10, 10, 3)) + [1, 0, 0])  # Red frame for '1'
        else:
            plt.imshow(np.zeros((10, 10, 3)) + [0, 0, 1])  # Blue frame for '0'
        plt.axis('off')
        frame_path = os.path.join(output_folder, f'frame_{i:04d}.png')
        plt.savefig(frame_path)
        plt.close()

def create_video_from_frames(frame_folder, output_video):
    """ Creates a video from frames stored in a folder. """
    images = sorted([img for img in os.listdir(frame_folder) if img.endswith(".png")],
                    key=lambda x: int(x.split('_')[1].split('.')[0]))
    frame = cv2.imread(os.path.join(frame_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width, height))
    
    for image in images:
        video.write(cv2.imread(os.path.join(frame_folder, image)))
    
    cv2.destroyAllWindows()
    video.release()

def main(text_input):
    binary_message = text_to_binary(text_input)
    print("Binary representation of the message:", binary_message)
    create_color_frames_from_binary(binary_message, 'frames')
    create_video_from_frames('frames', 'output_video.mp4')
    print("Video created successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert text to binary and visualize as frames and video.')
    parser.add_argument('-t', '--text', type=str, default="Up",
                        help='Text to convert to binary. Default is "Up".')
    args = parser.parse_args()
    
    main(args.text)

