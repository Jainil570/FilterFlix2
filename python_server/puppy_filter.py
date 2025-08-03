# puppy_filter.py
import cv2
import numpy as np
import mediapipe as mp
import math
import os

# --- MediaPipe FaceMesh Setup ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1
)

# --- Load Image ---
def load_image(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None: raise IOError(f"Could not load {filename}")
    if img.shape[2] != 4: raise ValueError(f"{filename} needs an alpha channel")
    return img

puppy_ears_img = load_image('puppy.png')

# --- Helper Functions ---
def overlay_transparent(background, overlay, x, y):
    bh, bw = background.shape[:2]
    h, w = overlay.shape[:2]
    if x >= bw or y >= bh or x + w <= 0 or y + h <= 0:
        return background  # completely out of bounds
    
    # Clip overlay area if going outside background
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + w, bw)
    y2 = min(y + h, bh)
    
    overlay_x1 = max(0, -x)
    overlay_y1 = max(0, -y)
    overlay_x2 = overlay_x1 + (x2 - x1)
    overlay_y2 = overlay_y1 + (y2 - y1)
    
    # Extract alpha channel and normalize
    alpha = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3:] / 255.0
    foreground = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, :3]
    background_crop = background[y1:y2, x1:x2]
    
    # Blend images
    blended = background_crop * (1 - alpha) + foreground * alpha
    background[y1:y2, x1:x2] = blended.astype(np.uint8)
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
    rotated = cv2.warpAffine(canvas, M, (canvas.shape[1], canvas.shape[0]), 
                            flags=cv2.INTER_LINEAR, 
                            borderMode=cv2.BORDER_CONSTANT, 
                            borderValue=(0,0,0,0))
    return rotated  # No cropping!

# --- Main Filter Function ---
def apply_puppy_filter(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            
            # Use forehead + sides of head
            top = face_landmarks.landmark[10]      # forehead top
            left = face_landmarks.landmark[127]    # left upper temple
            right = face_landmarks.landmark[356]   # right upper temple
            
            x_top = int(top.x * w)
            y_top = int(top.y * h)
            x_left = int(left.x * w)
            y_left = int(left.y * h)
            x_right = int(right.x * w)
            y_right = int(right.y * h)
            
            # Center and size
            ears_center_x = (x_left + x_right) // 2
            # Original positioning logic (very small adjustment)
            ears_center_y = y_top - int(abs(x_right - x_left) * 0.001)
            
            # Original sizing logic
            ears_width = int(abs(x_right - x_left) * 2)
            ears_height = int(ears_width * puppy_ears_img.shape[0] / puppy_ears_img.shape[1])
            
            # Calculate rotation angle based on head tilt
            angle = -math.degrees(math.atan2(y_right - y_left, x_right - x_left))
            
            # Resize and rotate ears (using original interpolation method)
            resized_ears = cv2.resize(puppy_ears_img, (ears_width, ears_height), 
                                    interpolation=cv2.INTER_AREA)
            rotated_ears = rotate_image(resized_ears, angle)
            
            # Overlay rotated ears
            rh, rw = rotated_ears.shape[:2]
            overlay_x = ears_center_x - rw // 2
            overlay_y = ears_center_y - rh // 2
            frame = overlay_transparent(frame, rotated_ears, overlay_x, overlay_y)
    
    return frame