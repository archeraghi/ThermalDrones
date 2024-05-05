from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

def gen_frames():
    """Generator to capture video stream and selectively process frames based on specific colors."""
    camera = cv2.VideoCapture(0)  # Use default camera
    start_detected = False
    binary_str = ""
    
    try:
        while True:
            success, frame = camera.read()
            if not success:
                break
            
            # Convert frame to HSV for more accurate color detection
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Define color ranges for start (green) and end (purple)
            green_lower = np.array([50, 100, 100], np.uint8)
            green_upper = np.array([70, 255, 255], np.uint8)
            purple_lower = np.array([130, 100, 100], np.uint8)
            purple_upper = np.array([160, 255, 255], np.uint8)
            
            # Create masks to detect specific colors
            green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)
            purple_mask = cv2.inRange(hsv_frame, purple_lower, purple_upper)
            
            if not start_detected:
                # Check if green start signal is detected
                if cv2.countNonZero(green_mask) > 50:
                    start_detected = True
            elif start_detected:
                # Check if purple end signal is detected
                if cv2.countNonZero(purple_mask) > 50:
                    break
                # Assuming red indicates binary '1'
                mean_color = np.mean(hsv_frame[:, :, 0])
                if mean_color > 150:  # Red-ish hue in HSV
                    binary_str += '1'
                else:
                    binary_str += '0'
            else:
                # If any other color interrupts before start is detected
                if cv2.countNonZero(green_mask) == 0 and cv2.countNonZero(purple_mask) == 0:
                    continue  # keep looking for the start signal
                else:
                    break  # terminate on unexpected colors

    finally:
        camera.release()  # Ensure the camera is released properly

    return binary_str

@app.route('/video_feed')
def video_feed():
    """Route to handle video stream."""
    binary_data = gen_frames()
    return Response(binary_data, mimetype='text/plain')

@app.route('/')
def index():
    """Home page to display the interface."""
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=5001)  # You can use any available port

