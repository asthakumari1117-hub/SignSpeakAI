"""
Session State Management
SignSpeak AI
"""

import streamlit as st
from datetime import datetime


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        # Navigation
        "current_page": "home",

        # Word & Sentence Builder
        "current_letters": [],
        "current_word": "",
        "sentence_words": [],
        "full_sentence": "",

        # Predictions
        "last_prediction": "",
        "last_confidence": 0.0,
        "total_predictions": 0,

        # History
        "prediction_history": [],

        # Settings
        "tts_enabled": True,
        "tts_engine": "gtts",
        "accessibility_mode": False,
        "large_text": False,
        "high_contrast": False,
        "dark_mode": True,

        # Statistics
        "sign_counts": {},
        "session_start": datetime.now().isoformat(),

        # Multi-language
        "output_language": "English",
        "translated_text": "",

        # Emergency mode
        "emergency_active": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
