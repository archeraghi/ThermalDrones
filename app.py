from flask import Flask, render_template, request
import numpy as np
from PIL import Image
import os
import shutil
import cv2

app = Flask(__name__)

def text_to_binary(text):
    """ Converts text to a binary string based on ASCII values. """
    return ''.join(format(ord(char), '08b') for char in text)

def create_color_frames_from_binary(binary_sequence, output_folder):
    """ Creates color frames based on the binary sequence where '1' is red and '0' is blue,
        with unique green start and purple end frames. """
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Add a start frame with a unique color (e.g., green)
    start_image = Image.new("RGB", (100, 100), (0, 255, 0))  # Green
    start_image.save(os.path.join(output_folder, 'frame_0000.png'))

    for i, bit in enumerate(binary_sequence, start=1):
        color = (255, 0, 0) if bit == '1' else (0, 0, 255)  # Red for '1', Blue for '0'
        image = Image.new("RGB", (100, 100), color)
        frame_path = os.path.join(output_folder, f'frame_{i:04d}.png')
        image.save(frame_path)

    # Add an end frame with a unique color (e.g., purple)
    end_image = Image.new("RGB", (100, 100), (128, 0, 128))  # Purple
    end_image.save(os.path.join(output_folder, f'frame_{len(binary_sequence) + 1:04d}.png'))

def create_video_from_frames(frame_folder, output_video):
    images = sorted([img for img in os.listdir(frame_folder) if img.endswith(".png")],
                    key=lambda x: int(x.split('_')[1].split('.')[0]))
    frame = cv2.imread(os.path.join(frame_folder, images[0]))
    height, width, layers = frame.shape
    # Increase frame rate from 1 fps to 10 fps
    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(frame_folder, image)))

    video.release()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        binary_message = text_to_binary(text)
        create_color_frames_from_binary(binary_message, 'static/frames')
        create_video_from_frames('static/frames', 'static/output_video.mp4')
        return render_template('index.html', video_exists=True)
    return render_template('index.html', video_exists=False)

if __name__ == "__main__":
    app.run(debug=True)

