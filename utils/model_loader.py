"""
Model Loader - Generic Pre-trained Model Loader
SignSpeak AI

Supports:
- .pkl / .pickle  (scikit-learn, etc.)
- .h5 / .keras    (TensorFlow / Keras)
- .tflite         (TensorFlow Lite)
- .pt / .pth      (PyTorch)

NO training code. Load & predict only.
"""

import os
import numpy as np
import streamlit as st

# ─── Supported model types ─────────────────────────────────────────────────────
MODEL_EXTENSIONS = [".pkl", ".pickle", ".h5", ".keras", ".tflite", ".pt", ".pth"]

# ─── Label maps ────────────────────────────────────────────────────────────────
ALPHABET_LABELS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

GESTURE_LABELS = [
    "Hello", "Thank You", "Yes", "No", "Good Morning",
    "Good Night", "Please", "Sorry", "Help", "I Love You",
    "Welcome", "Bye", "Nice To Meet You", "How Are You", "Fine",
    "Hungry", "Water", "Emergency", "Doctor", "Hospital",
    "Police", "Friend", "Family", "Mother", "Father",
    "Brother", "Sister", "Food", "Drink", "Stop",
    "Go", "Come", "Wait",
]

ALL_LABELS = ALPHABET_LABELS + GESTURE_LABELS


# ─── Model class ───────────────────────────────────────────────────────────────
class SignModel:
    """
    Generic wrapper for a pre-trained sign-language model.
    Automatically detects model type from file extension.
    """

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.model_type = None
        self._load()

    def _load(self):
        ext = os.path.splitext(self.model_path)[1].lower()

        if ext in (".pkl", ".pickle"):
            self._load_sklearn()
        elif ext in (".h5", ".keras"):
            self._load_keras()
        elif ext == ".tflite":
            self._load_tflite()
        elif ext in (".pt", ".pth"):
            self._load_torch()
        else:
            raise ValueError(f"Unsupported model format: {ext}")

    # ── Sklearn / Pickle ──────────────────────────────────────────────────────
    def _load_sklearn(self):
        import pickle
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)
        self.model_type = "sklearn"

    def _predict_sklearn(self, features: np.ndarray):
        proba = self.model.predict_proba([features])[0]
        idx = int(np.argmax(proba))
        return idx, float(proba[idx])

    # ── Keras / H5 ────────────────────────────────────────────────────────────
    def _load_keras(self):
        try:
            import tensorflow as tf
            self.model = tf.keras.models.load_model(self.model_path)
            self.model_type = "keras"
        except ImportError:
            raise ImportError("TensorFlow is required for .h5/.keras models. Install: pip install tensorflow")

    def _predict_keras(self, features: np.ndarray):
        inp = features.reshape(1, -1)
        proba = self.model.predict(inp, verbose=0)[0]
        idx = int(np.argmax(proba))
        return idx, float(proba[idx])

    # ── TFLite ───────────────────────────────────────────────────────────────
    def _load_tflite(self):
        try:
            import tensorflow as tf
            self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
            self.interpreter.allocate_tensors()
            self.input_details  = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.model_type = "tflite"
        except ImportError:
            raise ImportError("TensorFlow is required for .tflite models.")

    def _predict_tflite(self, features: np.ndarray):
        inp = features.reshape(1, -1).astype(np.float32)
        self.interpreter.set_tensor(self.input_details[0]["index"], inp)
        self.interpreter.invoke()
        proba = self.interpreter.get_tensor(self.output_details[0]["index"])[0]
        idx = int(np.argmax(proba))
        return idx, float(proba[idx])

    # ── PyTorch ───────────────────────────────────────────────────────────────
    def _load_torch(self):
        try:
            import torch
            self.model = torch.load(self.model_path, map_location="cpu")
            self.model.eval()
            self.model_type = "torch"
        except ImportError:
            raise ImportError("PyTorch is required for .pt/.pth models. Install: pip install torch")

    def _predict_torch(self, features: np.ndarray):
        import torch
        inp = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            out = self.model(inp)
            proba = torch.softmax(out, dim=1).numpy()[0]
        idx = int(np.argmax(proba))
        return idx, float(proba[idx])

    # ── Unified predict ───────────────────────────────────────────────────────
    def predict(self, features: np.ndarray, label_set: list = None) -> dict:
        """
        Run prediction on extracted features.

        Args:
            features:  1-D numpy array of hand landmark features
            label_set: list of class names (defaults to ALL_LABELS)

        Returns:
            dict with keys: label, confidence, all_probs
        """
        labels = label_set or ALL_LABELS

        dispatch = {
            "sklearn": self._predict_sklearn,
            "keras":   self._predict_keras,
            "tflite":  self._predict_tflite,
            "torch":   self._predict_torch,
        }

        idx, conf = dispatch[self.model_type](features)
        label = labels[idx] if idx < len(labels) else f"Class_{idx}"

        return {
            "label":      label,
            "confidence": round(conf * 100, 2),
            "class_idx":  idx,
        }


# ─── Cached model loader ───────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(model_path: str) -> SignModel | None:
    """
    Load the model once and cache it across all sessions.
    Returns None if no model file is found.
    """
    if not os.path.exists(model_path):
        return None
    try:
        return SignModel(model_path)
    except Exception as e:
        st.error(f"⚠️ Model load error: {e}")
        return None


def find_model() -> str | None:
    """
    Scan the models/ directory for any supported model file.
    Returns the first one found, or None.
    """
    models_dir = "models"
    if not os.path.isdir(models_dir):
        return None

    for fname in os.listdir(models_dir):
        ext = os.path.splitext(fname)[1].lower()
        if ext in MODEL_EXTENSIONS:
            return os.path.join(models_dir, fname)

    return None


def get_model() -> SignModel | None:
    """Convenience: find + load the model."""
    path = find_model()
    if path is None:
        return None
    return load_model(path)
