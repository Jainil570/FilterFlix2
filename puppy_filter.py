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
def apply_puppy_filter(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            top, left, right = face_landmarks.landmark[10], face_landmarks.landmark[127], face_landmarks.landmark[356]
            x_left, y_left, x_right, y_right, y_top = int(left.x * w), int(left.y * h), int(right.x * w), int(right.y * h), int(top.y * h)
            ears_center_x = (x_left + x_right) // 2
            ears_center_y = y_top - int(abs(x_right - x_left) * 0.1)
            ears_width = int(abs(x_right - x_left) * 1.5)
            angle = -math.degrees(math.atan2(y_right - y_left, x_right - x_left))
            aspect_ratio = puppy_ears_img.shape[0] / puppy_ears_img.shape[1]
            ears_height = int(ears_width * aspect_ratio)
            resized_ears = cv2.resize(puppy_ears_img, (ears_width, ears_height))
            rotated_ears = rotate_image(resized_ears, angle)
            rh, rw = rotated_ears.shape[:2]
            frame = overlay_transparent(frame, rotated_ears, ears_center_x - rw // 2, ears_center_y - rh // 2)
    return frame
