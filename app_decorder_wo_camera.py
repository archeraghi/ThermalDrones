from flask import Flask, render_template
import os
import cv2
import numpy as np
import time

app = Flask(__name__)

def video_to_binary(video_path):
    """Extracts frames from the video and decodes them into a binary string, ignoring start/end frames."""
    cap = cv2.VideoCapture(video_path)
    binary_str = ""
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        if i == 0 or i == frame_count - 1:  # Skip the first and the last frame
            continue
        if np.mean(frame[:, :, 2]) > 128:  # Check if the red channel is dominant
            binary_str += '1'
        else:
            binary_str += '0'
    cap.release()
    return binary_str

def binary_to_text(binary_str):
    """Converts a binary string to ASCII text."""
    n = 8
    text = ''.join(chr(int(binary_str[i:i+n], 2)) for i in range(0, len(binary_str), n))
    return text

@app.route('/')
def index():
    video_path = 'static/output_video.mp4'
    if os.path.exists(video_path):
        binary_message = video_to_binary(video_path)
        decoded_text = binary_to_text(binary_message)
        return render_template('index2V.html', decoded_text=decoded_text)
    return render_template('index2V.html', decoded_text="No video available")

if __name__ == "__main__":
    app.run(debug=True, port=5001)

