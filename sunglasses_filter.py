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
def overlay_transparent(background, overlay, x, y):
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
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

# --- Main Filter Function ---
def apply_sunglasses_filter(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            left_eye, right_eye = face_landmarks.landmark[33], face_landmarks.landmark[263]
            x1, y1, x2, y2 = int(left_eye.x * w), int(left_eye.y * h), int(right_eye.x * w), int(right_eye.y * h)
            center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)
            glasses_width = int(abs(x2 - x1) * 1.8)
            angle = -math.degrees(math.atan2(y2 - y1, x2 - x1))
            aspect_ratio = sunglasses_img.shape[0] / sunglasses_img.shape[1]
            glasses_height = int(glasses_width * aspect_ratio)
            resized_glasses = cv2.resize(sunglasses_img, (glasses_width, glasses_height))
            rotated_glasses = rotate_image(resized_glasses, angle)
            rh, rw = rotated_glasses.shape[:2]
            frame = overlay_transparent(frame, rotated_glasses, center_x - rw // 2, center_y - rh // 2)
    return frame
