# crown_filter.py
import cv2
import mediapipe as mp
import numpy as np
import os
import math

# --- MediaPipe FaceMesh Setup ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, 
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --- Load Image ---
def load_image(filename):
    """Loads a transparent PNG image from the same directory."""
    path = os.path.join(os.path.dirname(__file__), filename)
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise IOError(f"Could not load {filename}. Make sure it's in the same directory.")
    if img.shape[2] != 4:
        raise ValueError(f"{filename} must have an alpha (transparency) channel.")
    return img

crown_img = load_image('crown.png')

# --- Helper Functions ---
def overlay_transparent(background, overlay, x, y):
    """Overlays a transparent RGBA image onto a BGR image, handling out-of-bounds cases."""
    bg_h, bg_w, _ = background.shape
    h, w, _ = overlay.shape
    x1, y1 = max(x, 0), max(y, 0)
    x2, y2 = min(x + w, bg_w), min(y + h, bg_h)
    if x2 <= x1 or y2 <= y1: return background
    overlay_x1, overlay_y1 = max(0, -x), max(0, -y)
    overlay_x2, overlay_y2 = overlay_x1 + (x2 - x1), overlay_y1 + (y2 - y1)
    alpha = overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, 3] / 255.0
    mask = np.dstack([alpha] * 3)
    roi = background[y1:y2, x1:x2]
    blended_roi = (1.0 - mask) * roi + mask * overlay[overlay_y1:overlay_y2, overlay_x1:overlay_x2, :3]
    background[y1:y2, x1:x2] = blended_roi.astype(np.uint8)
    return background

def rotate_image(image, angle):
    """Rotates an RGBA image around its center without cropping."""
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

# --- Main Filter Function ---
def apply_crown_filter(frame):
    """Applies a crown filter to a face detected in the frame."""
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            
            # Get landmarks for forehead and temples
            left_temple = face_landmarks.landmark[127]
            right_temple = face_landmarks.landmark[356]
            forehead_top = face_landmarks.landmark[10]

            x_left, y_left = int(left_temple.x * w), int(left_temple.y * h)
            x_right, y_right = int(right_temple.x * w), int(right_temple.y * h)
            y_top = int(forehead_top.y * h)

            # Calculate angle for head tilt
            angle = -math.degrees(math.atan2(y_right - y_left, x_right - x_left))

            # Calculate width and height of the crown
            crown_width = int(abs(x_right - x_left) * 1.5)
            aspect_ratio = crown_img.shape[0] / crown_img.shape[1]
            crown_height = int(crown_width * aspect_ratio)

            # Resize and rotate the crown image
            resized_crown = cv2.resize(crown_img, (crown_width, crown_height))
            rotated_crown = rotate_image(resized_crown, angle)

            # Calculate position to place the crown
            rh, rw = rotated_crown.shape[:2]
            center_x = (x_left + x_right) // 2
            
            # Position the crown above the forehead
            pos_x = center_x - (rw // 2)
            pos_y = y_top - int(rh * 0.9) # Adjust the 0.9 to move up/down
            
            # Overlay the crown on the frame
            frame = overlay_transparent(frame, rotated_crown, pos_x, pos_y)

    return frame
