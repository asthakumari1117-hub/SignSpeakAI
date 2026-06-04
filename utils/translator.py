"""
Multi-Language Translation Utility
Uses deep-translator (free, no API key required)
SignSpeak AI
"""

import streamlit as st

SUPPORTED_LANGUAGES = {
    "English":  "en",
    "Hindi":    "hi",
    "Punjabi":  "pa",
    "French":   "fr",
    "Spanish":  "es",
    "German":   "de",
    "Arabic":   "ar",
}


def translate_text(text: str, target_language: str) -> str:
    """
    Translate text to target language.
    Returns original text if translation fails.
    """
    if not text or not text.strip():
        return text

    if target_language == "English":
        return text

    target_code = SUPPORTED_LANGUAGES.get(target_language, "en")

    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="en", target=target_code).translate(text)
        return translated or text
    except ImportError:
        try:
            from googletrans import Translator
            translator = Translator()
            result = translator.translate(text, dest=target_code)
            return result.text or text
        except Exception:
            return f"[{text}]"
    except Exception:
        return text


def language_selector(key: str = "lang_select") -> str:
    """Render a language selector widget."""
    current = st.session_state.get("output_language", "English")
    selected = st.selectbox(
        "🌐 Output Language",
        list(SUPPORTED_LANGUAGES.keys()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(current),
        key=key,
    )
    st.session_state.output_language = selected
    return selected
