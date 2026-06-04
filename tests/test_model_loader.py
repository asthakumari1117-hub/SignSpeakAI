"""
Unit Tests — Model Loader & Utilities
SignSpeak AI
Run: pytest tests/ -v
"""

import sys
import os
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.model_loader import (
    find_model,
    ALPHABET_LABELS,
    GESTURE_LABELS,
    ALL_LABELS,
)
from utils.demo_predictor import get_demo_prediction, DemoPredictor
from utils.history_utils import record_prediction, load_history_df
from utils.translator import translate_text, SUPPORTED_LANGUAGES
from utils.hand_extractor import normalize_features


# ─── Label Maps ───────────────────────────────────────────────────────────────

class TestLabelMaps:
    def test_alphabet_labels_count(self):
        assert len(ALPHABET_LABELS) == 26

    def test_alphabet_labels_content(self):
        assert "A" in ALPHABET_LABELS
        assert "Z" in ALPHABET_LABELS

    def test_gesture_labels_count(self):
        assert len(GESTURE_LABELS) == 33

    def test_all_labels_combined(self):
        assert len(ALL_LABELS) == len(ALPHABET_LABELS) + len(GESTURE_LABELS)

    def test_no_duplicates_in_alphabet(self):
        assert len(ALPHABET_LABELS) == len(set(ALPHABET_LABELS))

    def test_no_duplicates_in_gestures(self):
        assert len(GESTURE_LABELS) == len(set(GESTURE_LABELS))


# ─── Demo Predictor ───────────────────────────────────────────────────────────

class TestDemoPredictor:
    def setup_method(self):
        self.predictor = DemoPredictor()

    def test_predict_alphabet_returns_dict(self):
        result = self.predictor.predict_alphabet()
        assert isinstance(result, dict)
        assert "label" in result
        assert "confidence" in result

    def test_predict_alphabet_label_valid(self):
        for _ in range(26):
            result = self.predictor.predict_alphabet()
            assert result["label"] in ALPHABET_LABELS

    def test_predict_gesture_returns_valid(self):
        result = self.predictor.predict_gesture()
        assert result["label"] in GESTURE_LABELS

    def test_confidence_range(self):
        result = self.predictor.predict_alphabet()
        assert 0 <= result["confidence"] <= 100

    def test_get_demo_prediction_alphabet(self):
        result = get_demo_prediction("alphabet")
        assert result["label"] in ALPHABET_LABELS

    def test_get_demo_prediction_gesture(self):
        result = get_demo_prediction("gesture")
        assert result["label"] in GESTURE_LABELS

    def test_get_demo_prediction_image(self):
        result = get_demo_prediction("image")
        assert "label" in result
        assert "confidence" in result

    def test_demo_flag_set(self):
        result = get_demo_prediction("alphabet")
        assert result.get("demo") is True


# ─── Feature Normalization ────────────────────────────────────────────────────

class TestHandExtractor:
    def test_normalize_features_range(self):
        features = np.array([1.0, 5.0, 3.0, 2.0, 8.0], dtype=np.float32)
        normalized = normalize_features(features)
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0

    def test_normalize_constant_features(self):
        """Should not crash on constant-value features."""
        features = np.ones(63, dtype=np.float32)
        result = normalize_features(features)
        assert result is not None

    def test_normalize_preserves_shape(self):
        features = np.random.rand(63).astype(np.float32)
        result = normalize_features(features)
        assert result.shape == features.shape


# ─── Translator ───────────────────────────────────────────────────────────────

class TestTranslator:
    def test_supported_languages_count(self):
        assert len(SUPPORTED_LANGUAGES) == 7

    def test_english_passthrough(self):
        """English→English should return unchanged text."""
        result = translate_text("Hello", "English")
        assert result == "Hello"

    def test_empty_string(self):
        result = translate_text("", "Hindi")
        assert result == ""

    def test_none_text(self):
        result = translate_text(None, "Hindi")
        assert result is None

    def test_language_codes_present(self):
        assert "en" in SUPPORTED_LANGUAGES.values()
        assert "hi" in SUPPORTED_LANGUAGES.values()
        assert "fr" in SUPPORTED_LANGUAGES.values()


# ─── History Utilities ────────────────────────────────────────────────────────

class TestHistoryUtils:
    def test_load_history_empty(self, monkeypatch):
        """Should return empty DataFrame when no history."""
        import streamlit as st

        class FakeSessionState(dict):
            pass

        fake = FakeSessionState(prediction_history=[])
        monkeypatch.setattr("streamlit.session_state", fake)
        df = load_history_df()
        assert df.empty

    def test_history_df_columns(self, monkeypatch):
        import streamlit as st

        fake_history = [
            {"time": "10:00:00", "date": "2024-01-01", "sign": "A",
             "confidence": 92.0, "mode": "live"},
        ]

        class FakeSession(dict):
            pass

        monkeypatch.setattr("streamlit.session_state", FakeSession(prediction_history=fake_history))
        df = load_history_df()
        assert "sign" in df.columns
        assert "confidence" in df.columns


# ─── Model Finder ─────────────────────────────────────────────────────────────

class TestFindModel:
    def test_find_model_returns_none_when_empty(self, tmp_path, monkeypatch):
        """find_model() should return None when models/ dir is empty."""
        models_dir = tmp_path / "models"
        models_dir.mkdir()
        monkeypatch.chdir(tmp_path)
        result = find_model()
        assert result is None

    def test_find_model_detects_pkl(self, tmp_path, monkeypatch):
        models_dir = tmp_path / "models"
        models_dir.mkdir()
        dummy = models_dir / "sign_model.pkl"
        import pickle
        dummy.write_bytes(pickle.dumps({"dummy": True}))
        monkeypatch.chdir(tmp_path)
        result = find_model()
        assert result is not None
        assert result.endswith(".pkl")
