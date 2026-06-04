"""
Hand Landmark Feature Extractor
Uses MediaPipe Hands to extract 21-landmark features from images/frames.
SignSpeak AI
"""

import numpy as np
import cv2
from typing import Optional, Tuple


def get_mediapipe():
    """Lazy import of mediapipe to handle version issues gracefully."""
    try:
        import mediapipe as mp
        return mp
    except ImportError:
        return None


class HandExtractor:
    """
    Extracts normalized hand landmark features from images.
    Output: 63-dimensional feature vector (21 landmarks × x,y,z).
    """

    def __init__(self, max_hands: int = 1, detection_conf: float = 0.6, tracking_conf: float = 0.5):
        mp = get_mediapipe()
        if mp is None:
            self.hands = None
            self.mp_drawing = None
            self.mp_hands = None
            return

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )

    @property
    def available(self) -> bool:
        return self.hands is not None

    def extract(self, frame_bgr: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract 63-dim feature vector from a BGR frame.
        Returns None if no hand is detected.
        """
        if not self.available:
            return None

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        if not results.multi_hand_landmarks:
            return None

        hand_landmarks = results.multi_hand_landmarks[0]

        # Collect x,y,z for all 21 landmarks
        coords = []
        for lm in hand_landmarks.landmark:
            coords.extend([lm.x, lm.y, lm.z])

        features = np.array(coords, dtype=np.float32)

        # Normalize: subtract wrist position (landmark 0)
        wrist = features[:3]
        for i in range(0, len(features), 3):
            features[i]   -= wrist[0]
            features[i+1] -= wrist[1]
            features[i+2] -= wrist[2]

        return features

    def draw_landmarks(self, frame_bgr: np.ndarray) -> Tuple[np.ndarray, bool]:
        """
        Draw hand landmarks on the frame.
        Returns (annotated_frame, hand_detected).
        """
        if not self.available:
            return frame_bgr, False

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        frame_out = frame_bgr.copy()
        detected = False

        if results.multi_hand_landmarks:
            detected = True
            for hand_lm in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame_out,
                    hand_lm,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

        return frame_out, detected

    def close(self):
        if self.hands:
            self.hands.close()


# ─── Image preprocessing ───────────────────────────────────────────────────────
def preprocess_image(image_bytes: bytes) -> Optional[np.ndarray]:
    """
    Convert uploaded image bytes to BGR numpy array.
    """
    try:
        import PIL.Image
        import io
        img = PIL.Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img)
        return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    except Exception:
        return None


def normalize_features(features: np.ndarray) -> np.ndarray:
    """Min-max normalize feature vector to [0, 1]."""
    mn, mx = features.min(), features.max()
    if mx - mn < 1e-8:
        return features
    return (features - mn) / (mx - mn)
