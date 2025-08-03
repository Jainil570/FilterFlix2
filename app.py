from flask import Flask, Response, jsonify, request, send_from_directory, make_response
from flask_cors import CORS
import cv2
import threading
import os
import zipfile
import io

# Import filter functions
from sunglasses_filter import apply_sunglasses_filter
from puppy_filter import apply_puppy_filter
from lipstick_filter import apply_lipstick_filter
from crown_filter import apply_crown_filter

app = Flask(__name__)
CORS(app, origins="http://localhost:8080", supports_credentials=True)

# Setup capture directory
CAPTURES_DIR = os.path.join(os.path.dirname(__file__), 'captures')
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)

active_filter = "none"
camera = cv2.VideoCapture(0)
global_frame = None
frame_lock = threading.Lock()

def get_user_folder(user_id):
    """Gets or creates a unique folder for the user ID."""
    user_folder = os.path.join(CAPTURES_DIR, user_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

def generate_frames():
    """Generator function for streaming filtered frames."""
    global global_frame, active_filter
    while True:
        success, frame = camera.read()
        if not success:
            break
        processed_frame = frame.copy()
        if active_filter == "sunglasses":
            processed_frame = apply_sunglasses_filter(processed_frame)
        elif active_filter == "puppy":
            processed_frame = apply_puppy_filter(processed_frame)
        elif active_filter == "lipstick":
            processed_frame = apply_lipstick_filter(processed_frame)
        elif active_filter == "crown":
            processed_frame = apply_crown_filter(processed_frame)

        with frame_lock:
            global_frame = processed_frame.copy()

        ret, buffer = cv2.imencode('.jpg', processed_frame)
        if not ret: continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify(success=False, message="Missing user_id")

    user_folder = get_user_folder(user_id)
    capture_count = len([name for name in os.listdir(user_folder) if name.endswith('.jpg')])
    filename = f"capture_{capture_count + 1}.jpg"

    with frame_lock:
        if global_frame is not None:
            cv2.imwrite(os.path.join(user_folder, filename), global_frame)
            return jsonify(success=True, message=f"Image saved as {filename}")
        return jsonify(success=False, message="Could not capture frame.")

@app.route('/set_filter', methods=['POST'])
def set_filter():
    global active_filter
    data = request.get_json()
    filter_name = data.get('filter', 'none')
    if filter_name in ["sunglasses", "puppy", "lipstick", "crown", "none"]:
        active_filter = filter_name
        return jsonify(success=True, message=f"Filter set to: {active_filter}")
    return jsonify(success=False, message="Invalid filter name"), 400

@app.route('/get_captures', methods=['GET'])
def get_captures():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify(success=False, files=[], message="Missing user_id")

    user_folder = get_user_folder(user_id)
    try:
        files = sorted([f for f in os.listdir(user_folder) if f.endswith('.jpg')])
        return jsonify(success=True, files=files)
    except FileNotFoundError:
        return jsonify(success=True, files=[])

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    user_id = request.args.get('user_id')
    if not user_id:
        return "Missing user_id", 400
    user_folder = get_user_folder(user_id)
    return send_from_directory(user_folder, filename, as_attachment=True)

@app.route('/download_all', methods=['GET'])
def download_all():
    user_id = request.args.get('user_id')
    if not user_id:
        return "Missing user_id", 400
    user_folder = get_user_folder(user_id)
    files = [f for f in os.listdir(user_folder) if f.endswith('.jpg')]

    if not files:
        return "No files to download.", 404

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for filename in files:
            zf.write(os.path.join(user_folder, filename), arcname=filename)
    memory_file.seek(0)

    response = make_response(memory_file.read())
    response.headers.set('Content-Type', 'application/zip')
    response.headers.set('Content-Disposition', 'attachment', filename='captures.zip')
    return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
