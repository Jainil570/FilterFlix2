# sunglasses_filter.py
import cv2
import numpy as np
import mediapipe as mp
import math
import os

# --- MediaPipe FaceMesh Setup ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, 
    max_num_faces=5, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5
)

# --- Load Image ---
def load_image(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None: raise IOError(f"Could not load {filename}")
    if img.shape[2] != 4: raise ValueError(f"{filename} needs an alpha channel")
    return img

sunglasses_img = load_image('sunglasses.png')

# --- Helper Functions ---
def overlay_transparent(background, overlay, x, y, overlay_size=None):
    bg_h, bg_w = background.shape[:2]
    if overlay_size:
        overlay = cv2.resize(overlay, overlay_size)
    h, w = overlay.shape[:2]
    if x < 0 or y < 0 or x + w > bg_w or y + h > bg_h:
        return background
    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0
    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image
    return background

def rotate_image(image, angle):
    """Rotate image (with alpha) around its center, using a larger canvas to avoid cropping."""
    h, w = image.shape[:2]
    canvas_size = (max(h, w) * 2, max(h, w) * 2, 4)
    canvas = np.zeros(canvas_size, dtype=np.uint8)
    y_offset = (canvas.shape[0] - h) // 2
    x_offset = (canvas.shape[1] - w) // 2
    canvas[y_offset:y_offset+h, x_offset:x_offset+w] = image
    center = (canvas.shape[1] // 2, canvas.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(canvas, M, (canvas.shape[1], canvas.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    return rotated  # No cropping!

# --- Main Filter Function ---
def apply_sunglasses_filter(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            
            # Sunglasses position: use eye corners
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]
            x1, y1 = int(left_eye.x * w), int(left_eye.y * h)
            x2, y2 = int(right_eye.x * w), int(right_eye.y * h)
            
            # Calculate center position with slight downward shift (like in original)
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2) + int(abs(x2 - x1) * 0.1)  # Shift sunglasses down slightly
            
            # Calculate sunglasses size
            glasses_width = int(abs(x2 - x1) * 1.8)
            glasses_height = int(glasses_width * sunglasses_img.shape[0] / sunglasses_img.shape[1])
            
            # Calculate rotation angle
            angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            
            # Resize and rotate the sunglasses
            resized_glasses = cv2.resize(sunglasses_img, (glasses_width, glasses_height), interpolation=cv2.INTER_AREA)
            rotated_glasses = rotate_image(resized_glasses, angle)
            
            # Calculate new position after rotation
            rh, rw = rotated_glasses.shape[:2]
            overlay_x = center_x - rw // 2
            overlay_y = center_y - rh // 2
            
            # Overlay the rotated sunglasses
            frame = overlay_transparent(
                frame,
                rotated_glasses,
                overlay_x,
                overlay_y
            )
    
    return frame