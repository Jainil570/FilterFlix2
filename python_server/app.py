from flask import Flask, Response, jsonify, request, send_from_directory, make_response
from flask_cors import CORS
import cv2
import threading
import os
import zipfile
import io
import time
from datetime import datetime

# Import filter functions
from sunglasses_filter import apply_sunglasses_filter
from puppy_filter import apply_puppy_filter
from lipstick_filter import apply_lipstick_filter
from crown_filter import apply_crown_filter

app = Flask(__name__)
CORS(app, origins="https://filterflix-frontend.onrender.com", supports_credentials=True)

# Setup capture directory
CAPTURES_DIR = os.path.join(os.path.dirname(__file__), 'captures')
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)

active_filter = "none"
camera = None
global_frame = None
frame_lock = threading.Lock()
camera_lock = threading.Lock()

def get_user_folder(user_id):
    """Gets or creates a unique folder for the user ID."""
    user_folder = os.path.join(CAPTURES_DIR, user_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

def initialize_camera():
    """Initialize camera with error handling."""
    global camera
    with camera_lock:
        if camera is None:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                print("Warning: Could not open camera")
                return False
            # Set camera properties for better quality
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            camera.set(cv2.CAP_PROP_FPS, 30)
    return True

def generate_frames():
    """Generator function for streaming filtered frames."""
    global global_frame, active_filter, camera
    
    if not initialize_camera():
        return
    
    while True:
        with camera_lock:
            if camera is None or not camera.isOpened():
                break
            success, frame = camera.read()
        
        if not success:
            print("Failed to read frame from camera")
            break
            
        # Apply filters
        processed_frame = frame.copy()
        try:
            if active_filter == "sunglasses":
                processed_frame = apply_sunglasses_filter(processed_frame)
            elif active_filter == "puppy":
                processed_frame = apply_puppy_filter(processed_frame)
            elif active_filter == "lipstick":
                processed_frame = apply_lipstick_filter(processed_frame)
            elif active_filter == "crown":
                processed_frame = apply_crown_filter(processed_frame)
        except Exception as e:
            print(f"Filter error: {e}")
            # Use original frame if filter fails
            processed_frame = frame

        # Store frame for capture
        with frame_lock:
            global_frame = processed_frame.copy()

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', processed_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    try:
        return Response(generate_frames(), 
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Video feed error: {e}")
        return jsonify(success=False, message="Camera not available"), 500

@app.route('/capture', methods=['POST'])
def capture():
    """Capture current frame and save it."""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return jsonify(success=False, message="Missing user_id"), 400

        user_folder = get_user_folder(user_id)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_count = len([name for name in os.listdir(user_folder) if name.endswith('.jpg')])
        filename = f"capture_{capture_count + 1}_{timestamp}.jpg"

        with frame_lock:
            if global_frame is not None:
                filepath = os.path.join(user_folder, filename)
                success = cv2.imwrite(filepath, global_frame)
                if success:
                    return jsonify(success=True, message=f"📸 Photo saved as {filename}")
                else:
                    return jsonify(success=False, message="Failed to save image")
            else:
                return jsonify(success=False, message="No frame available to capture")
                
    except Exception as e:
        print(f"Capture error: {e}")
        return jsonify(success=False, message=f"Capture failed: {str(e)}"), 500
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_count = len([name for name in os.listdir(user_folder) if name.endswith('.jpg')])
        filename = f"capture_{capture_count + 1}_{timestamp}.jpg"

        with frame_lock:
            if global_frame is not None:
                filepath = os.path.join(user_folder, filename)
                success = cv2.imwrite(filepath, global_frame)
                if success:
                    return jsonify(success=True, message=f"📸 Photo saved as {filename}")
                else:
                    return jsonify(success=False, message="Failed to save image")
            else:
                return jsonify(success=False, message="No frame available to capture")
                
    except Exception as e:
        print(f"Capture error: {e}")
        return jsonify(success=False, message=f"Capture failed: {str(e)}"), 500

@app.route('/set_filter', methods=['POST'])
def set_filter():
    """Set the active filter."""
    global active_filter
    try:
        data = request.get_json()
        filter_name = data.get('filter', 'none')
        
        valid_filters = ["sunglasses", "puppy", "lipstick", "crown", "none"]
        if filter_name in valid_filters:
            active_filter = filter_name
            filter_display = "No filter" if filter_name == "none" else filter_name.title()
            return jsonify(success=True, message=f"✨ Filter set to: {filter_display}")
        else:
            return jsonify(success=False, message="Invalid filter name"), 400
            
    except Exception as e:
        print(f"Set filter error: {e}")
        return jsonify(success=False, message=f"Failed to set filter: {str(e)}"), 500

@app.route('/get_captures', methods=['GET'])
def get_captures():
    """Get list of captured images for a user."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify(success=False, files=[], message="Missing user_id")

        user_folder = get_user_folder(user_id)
        
        try:
            files = sorted([f for f in os.listdir(user_folder) if f.endswith('.jpg')], reverse=True)
            return jsonify(success=True, files=files)
        except FileNotFoundError:
            return jsonify(success=True, files=[])
            
    except Exception as e:
        print(f"Get captures error: {e}")
        return jsonify(success=False, files=[], message=f"Error: {str(e)}")

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a specific captured image."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return "Missing user_id", 400
            
        user_folder = get_user_folder(user_id)
        
        # Security check - ensure filename doesn't contain path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return "Invalid filename", 400
            
        file_path = os.path.join(user_folder, filename)
        if not os.path.exists(file_path):
            return "File not found", 404
            
        return send_from_directory(user_folder, filename, as_attachment=True)
        
    except Exception as e:
        print(f"Download error: {e}")
        return f"Download failed: {str(e)}", 500

@app.route('/download_all', methods=['GET'])
def download_all():
    """Download all captured images as a ZIP file."""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return "Missing user_id", 400
            
        user_folder = get_user_folder(user_id)
        files = [f for f in os.listdir(user_folder) if f.endswith('.jpg')]

        if not files:
            return "No files to download", 404

        # Create ZIP file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for filename in files:
                file_path = os.path.join(user_folder, filename)
                zf.write(file_path, arcname=filename)
        
        memory_file.seek(0)

        response = make_response(memory_file.read())
        response.headers.set('Content-Type', 'application/zip')
        response.headers.set('Content-Disposition', 'attachment', 
                           filename=f'snapfilter_captures_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip')
        return response
        
    except Exception as e:
        print(f"Download all error: {e}")
        return f"Download failed: {str(e)}", 500

@app.route('/camera_status', methods=['GET'])
def camera_status():
    """Check if camera is available."""
    global camera
    try:
        with camera_lock:
            if camera is None:
                test_camera = cv2.VideoCapture(0)
                available = test_camera.isOpened()
                test_camera.release()
            else:
                available = camera.isOpened()
        
        return jsonify(success=True, available=available)
    except Exception as e:
        print(f"Camera status error: {e}")
        return jsonify(success=False, available=False, message=str(e))

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    """Stop the camera and release resources."""
    global camera
    try:
        with camera_lock:
            if camera is not None:
                camera.release()
                camera = None
        return jsonify(success=True, message="Camera stopped")
    except Exception as e:
        print(f"Stop camera error: {e}")
        return jsonify(success=False, message=str(e))

@app.errorhandler(404)
def not_found(error):
    return jsonify(success=False, message="Endpoint not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(success=False, message="Internal server error"), 500

# Cleanup function
def cleanup():
    """Clean up resources on shutdown."""
    global camera
    if camera is not None:
        camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        print("🎭 SnapFilter Server Starting...")
        print("📷 Camera initializing...")
        print("🌐 Server running on http://localhost:5000")
        print("🎨 Ready for filtering!")
        
        app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        cleanup()
    except Exception as e:
        print(f"❌ Server error: {e}")
        cleanup()