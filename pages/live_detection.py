"""
Live Camera Detection Page
Real-time A-Z sign language detection via webcam
SignSpeak AI
"""

import streamlit as st
import numpy as np
import cv2
import time
from utils.model_loader import get_model, ALPHABET_LABELS
from utils.hand_extractor import HandExtractor
from utils.tts import speak_text, tts_controls
from utils.history_utils import record_prediction
from utils.demo_predictor import get_demo_prediction


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">📷 Live Detection</div>
            <div class="page-subtitle">Real-Time Sign Language Recognition</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model = get_model()
    is_demo = model is None

    if is_demo:
        st.markdown(
            """
            <div style="text-align:center; margin-bottom:1rem">
                <span class="badge badge-cyan"><span class="badge-dot"></span>
                DEMO MODE — Place your model in models/ to enable real detection</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Layout ──
    col_cam, col_result = st.columns([3, 2])

    with col_cam:
        st.markdown("<div class='section-header'>CAMERA FEED</div>", unsafe_allow_html=True)
        camera_input = st.camera_input(
            "Point your hand at the camera",
            key="live_cam",
            label_visibility="collapsed",
        )

        # Controls
        c1, c2, c3 = st.columns(3)
        with c1:
            add_letter = st.button("➕ Add Letter", use_container_width=True)
        with c2:
            clear_word = st.button("🗑️ Clear Word", use_container_width=True)
        with c3:
            finish_word = st.button("✅ Finish Word", use_container_width=True)

        tts_controls()

    with col_result:
        st.markdown("<div class='section-header'>PREDICTION</div>", unsafe_allow_html=True)

        # Prediction area (placeholder)
        pred_placeholder = st.empty()
        conf_placeholder = st.empty()

        # ── Process frame ──
        if camera_input is not None:
            # Read image
            img_bytes = camera_input.getvalue()
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is not None:
                if is_demo:
                    result = get_demo_prediction("alphabet")
                else:
                    extractor = HandExtractor()
                    features = extractor.extract(frame)
                    if features is not None:
                        result = model.predict(features, ALPHABET_LABELS)
                    else:
                        result = {"label": "—", "confidence": 0.0}

                label = result["label"]
                conf  = result["confidence"]

                # Store last prediction
                if label != "—":
                    st.session_state.last_prediction = label
                    st.session_state.last_confidence = conf

                # Display prediction
                pred_placeholder.markdown(
                    f"""
                    <div class="prediction-box">
                        <div class="prediction-letter">{label}</div>
                        <div class="confidence-label">Detected Sign</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Confidence bar
                conf_color = "#00ff88" if conf >= 80 else "#ffd60a" if conf >= 60 else "#ff2d55"
                conf_placeholder.markdown(
                    f"""
                    <div style="margin-top:12px">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px">
                            <span style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted)">CONFIDENCE</span>
                            <span style="font-family:var(--font-head); font-size:1.1rem; font-weight:700; color:{conf_color}">{conf}%</span>
                        </div>
                        <div class="conf-bar-wrap">
                            <div class="conf-bar-fill" style="width:{conf}%; background:linear-gradient(90deg, var(--blue), {conf_color})"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Add letter
                if add_letter and label != "—" and conf > 40:
                    st.session_state.current_letters.append(label)
                    st.session_state.current_word = "".join(st.session_state.current_letters)
                    record_prediction(label, conf, mode="live")
                    speak_text(label)

        else:
            pred_placeholder.markdown(
                """
                <div class="prediction-box" style="border-color: rgba(0,245,255,0.3)">
                    <div class="prediction-letter" style="color: rgba(0,245,255,0.3)">?</div>
                    <div class="confidence-label">Waiting for camera...</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Word & Sentence builder ──────────────────────────────────────────────
    st.markdown("<div class='section-header'>WORD BUILDER</div>", unsafe_allow_html=True)

    # Handle buttons
    if clear_word:
        st.session_state.current_letters = []
        st.session_state.current_word = ""
        st.rerun()

    if finish_word and st.session_state.current_word:
        st.session_state.sentence_words.append(st.session_state.current_word)
        st.session_state.full_sentence = " ".join(st.session_state.sentence_words)
        st.session_state.current_letters = []
        st.session_state.current_word = ""
        speak_text(st.session_state.full_sentence)
        st.rerun()

    # Current letters
    letters = st.session_state.get("current_letters", [])
    if letters:
        chips_html = "".join(f'<span class="letter-chip">{l}</span>' for l in letters)
        st.markdown(f'<div class="letter-chips">{chips_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="text-align:center; color:var(--text-muted); font-family:var(--font-mono); '
            'font-size:0.75rem; padding:12px">Start signing to add letters...</div>',
            unsafe_allow_html=True,
        )

    # Current word
    word = st.session_state.get("current_word", "")
    if word:
        st.markdown(f'<div class="word-display">{word}</div>', unsafe_allow_html=True)

    # Sentence
    sentence = st.session_state.get("full_sentence", "")
    if sentence:
        st.markdown("<div class='section-header'>SENTENCE</div>", unsafe_allow_html=True)
        st.markdown(f'<div class="sentence-display">{sentence}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🔊 Speak Sentence", use_container_width=True):
                speak_text(sentence)
        with c2:
            if st.button("🗑️ Clear Sentence", use_container_width=True):
                st.session_state.sentence_words = []
                st.session_state.full_sentence = ""
                st.rerun()
        with c3:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                st.code(sentence)

    # Recent history snippet
    history = st.session_state.get("prediction_history", [])[:5]
    if history:
        st.markdown("<div class='section-header'>RECENT DETECTIONS</div>", unsafe_allow_html=True)
        for entry in history:
            st.markdown(
                f"""
                <div class="history-row">
                    <span class="history-sign">{entry['sign']}</span>
                    <span class="history-conf">{entry['confidence']}%</span>
                    <span style="color:var(--text-muted); font-size:0.7rem">{entry.get('mode','live')}</span>
                    <span class="history-time">{entry['time']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
