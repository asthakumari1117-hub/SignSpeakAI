"""
Text-to-Speech Utility
Supports gTTS (cloud) and pyttsx3 (offline)
SignSpeak AI
"""

import streamlit as st
import os
import tempfile
import base64
from typing import Optional


def speak_text(text: str, engine: str = "gtts", lang: str = "en") -> bool:
    """
    Convert text to speech and play it in the browser.

    Args:
        text:   Text to speak
        engine: 'gtts' or 'pyttsx3'
        lang:   Language code for gTTS (default 'en')

    Returns:
        True if successful, False otherwise
    """
    if not text or not text.strip():
        return False

    if not st.session_state.get("tts_enabled", True):
        return False

    try:
        if engine == "gtts":
            return _speak_gtts(text, lang)
        else:
            return _speak_pyttsx3(text)
    except Exception as e:
        # Silently fall back — don't crash the app
        st.warning(f"🔇 TTS unavailable: {e}")
        return False


def _speak_gtts(text: str, lang: str = "en") -> bool:
    """Use gTTS to generate audio and auto-play via HTML."""
    try:
        from gtts import gTTS
    except ImportError:
        return _speak_pyttsx3(text)

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
            tts.save(tmp_path)

        with open(tmp_path, "rb") as f:
            audio_bytes = f.read()

        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay style="display:none">
            <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        os.unlink(tmp_path)
        return True

    except Exception:
        return False


def _speak_pyttsx3(text: str) -> bool:
    """Use pyttsx3 for offline TTS (local only, won't work on Streamlit Cloud)."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 0.9)
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        return False


def get_gtts_lang_code(language: str) -> str:
    """Map display language name to gTTS language code."""
    lang_map = {
        "English":  "en",
        "Hindi":    "hi",
        "Punjabi":  "pa",
        "French":   "fr",
        "Spanish":  "es",
        "German":   "de",
        "Arabic":   "ar",
    }
    return lang_map.get(language, "en")


def tts_controls():
    """Render mute/unmute button. Returns True if TTS is enabled."""
    enabled = st.session_state.get("tts_enabled", True)
    icon = "🔊" if enabled else "🔇"
    label = f"{icon} {'Mute' if enabled else 'Unmute'} Voice"

    if st.button(label, key="tts_toggle", use_container_width=True):
        st.session_state.tts_enabled = not enabled
        st.rerun()

    return st.session_state.get("tts_enabled", True)
