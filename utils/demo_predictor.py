"""
Demo Predictor - Fallback when no model is present
Simulates realistic predictions for demonstration
SignSpeak AI
"""

import random
import numpy as np
from utils.model_loader import ALPHABET_LABELS, GESTURE_LABELS, ALL_LABELS


class DemoPredictor:
    """
    Simulates sign language predictions for demonstration purposes.
    Used when no pre-trained model file is found in models/.
    """

    def __init__(self):
        self._letter_idx = 0
        self._gesture_idx = 0

    def predict_alphabet(self) -> dict:
        """Return a demo alphabet prediction."""
        label = ALPHABET_LABELS[self._letter_idx % len(ALPHABET_LABELS)]
        self._letter_idx += 1
        conf = round(random.uniform(75, 98), 2)
        return {"label": label, "confidence": conf, "demo": True}

    def predict_gesture(self) -> dict:
        """Return a demo gesture prediction."""
        label = GESTURE_LABELS[self._gesture_idx % len(GESTURE_LABELS)]
        self._gesture_idx += 1
        conf = round(random.uniform(70, 97), 2)
        return {"label": label, "confidence": conf, "demo": True}

    def predict_from_image(self) -> dict:
        """Return a demo prediction for an uploaded image."""
        label = random.choice(ALPHABET_LABELS[:10])
        conf  = round(random.uniform(72, 96), 2)
        return {"label": label, "confidence": conf, "demo": True}


_demo = DemoPredictor()


def get_demo_prediction(mode: str = "alphabet") -> dict:
    if mode == "gesture":
        return _demo.predict_gesture()
    elif mode == "image":
        return _demo.predict_from_image()
    return _demo.predict_alphabet()
