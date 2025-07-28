from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import cv2
import threading
import os

# --- 1. IMPORT THE FILTER FUNCTIONS FROM THEIR DEDICATED FILES ---
from sunglasses_filter import apply_sunglasses_filter
from puppy_filter import apply_puppy_filter

app = Flask(__name__)
CORS(app)

# Use a string to track the active filter
active_filter = "none" # Can be "none", "sunglasses", or "puppy"

capture_counter = 0
camera = cv2.VideoCapture(0)
global_frame = None
frame_lock = threading.Lock()

def generate_frames():
    """Generator function to capture frames, apply the active filter, and stream."""
    global global_frame, active_filter
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Apply the currently selected filter
            if active_filter == "sunglasses":
                frame = apply_sunglasses_filter(frame)
            elif active_filter == "puppy":
                frame = apply_puppy_filter(frame)

            with frame_lock:
                global_frame = frame.copy()
            
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret: continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    global capture_counter
    with frame_lock:
        if global_frame is not None:
            capture_counter += 1
            filename = f"capture{capture_counter}.jpg"
            cv2.imwrite(os.path.join(os.path.dirname(__file__), filename), global_frame)
            return jsonify(success=True, message=f"Image saved as {filename}")
        return jsonify(success=False, message="Could not capture frame.")

@app.route('/set_filter', methods=['POST'])
def set_filter():
    """Sets the active filter based on JSON data from the request."""
    global active_filter
    data = request.get_json()
    filter_name = data.get('filter', 'none')
    
    if filter_name in ["sunglasses", "puppy", "none"]:
        active_filter = filter_name
        return jsonify(success=True, message=f"Filter set to: {active_filter}")
    else:
        return jsonify(success=False, message="Invalid filter name"), 400

if __name__ == '__main__':
    # use_reloader=False is important to prevent global variables from resetting
    app.run(debug=True, use_reloader=False)
