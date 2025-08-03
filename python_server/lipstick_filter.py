# lipstick_filter.py
import cv2
import mediapipe as mp
import numpy as np

# --- MediaPipe FaceMesh Setup ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False, 
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# --- Lip Landmark Indices (for outer lips) ---
LIPS = [
    61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,
    185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78
]

# --- Main Filter Function ---
def apply_lipstick_filter(frame, lipstick_color=(0, 0, 255), alpha=0.6, scale_w=1.0, scale_h=1.0):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            
            # Extract lip landmarks
            lips_points = []
            for idx in LIPS:
                lm = face_landmarks.landmark[idx]
                x_lm, y_lm = int(lm.x * w), int(lm.y * h)
                lips_points.append([x_lm, y_lm])
            
            lips_points = np.array(lips_points, np.int32)
            
            # Scale lips region (for exaggeration)
            lips_center = np.mean(lips_points, axis=0)
            lips_points_scaled = []
            for pt in lips_points:
                dx = pt[0] - lips_center[0]
                dy = pt[1] - lips_center[1]
                new_x = int(lips_center[0] + dx * scale_w)
                new_y = int(lips_center[1] + dy * scale_h)
                lips_points_scaled.append([new_x, new_y])
            
            lips_points_scaled = np.array(lips_points_scaled, np.int32)
            
            # Create lipstick mask
            mask = np.zeros(frame.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [lips_points_scaled], 255)
            
            # Create a colored image for the lipstick
            colored_lips = np.zeros_like(frame)
            colored_lips[:] = lipstick_color
            
            # Blend only the lips region
            frame = np.where(mask[..., None] == 255,
                            cv2.addWeighted(frame, 1 - alpha, colored_lips, alpha, 0),
                            frame)
    
    return frame