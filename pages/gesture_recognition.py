"""
Gesture Recognition Page
Detects 33 common sign language gestures
SignSpeak AI
"""

import streamlit as st
import numpy as np
import cv2
from utils.model_loader import get_model, GESTURE_LABELS
from utils.hand_extractor import HandExtractor
from utils.tts import speak_text, tts_controls
from utils.history_utils import record_prediction
from utils.demo_predictor import get_demo_prediction


GESTURE_EMOJIS = {
    "Hello":          "👋",
    "Thank You":      "🙏",
    "Yes":            "✅",
    "No":             "❌",
    "Good Morning":   "🌅",
    "Good Night":     "🌙",
    "Please":         "🤲",
    "Sorry":          "😔",
    "Help":           "🆘",
    "I Love You":     "❤️",
    "Welcome":        "🤗",
    "Bye":            "👋",
    "Nice To Meet You":"😊",
    "How Are You":    "🤔",
    "Fine":           "👍",
    "Hungry":         "🍽️",
    "Water":          "💧",
    "Emergency":      "🚨",
    "Doctor":         "👨‍⚕️",
    "Hospital":       "🏥",
    "Police":         "👮",
    "Friend":         "🤝",
    "Family":         "👨‍👩‍👧",
    "Mother":         "👩",
    "Father":         "👨",
    "Brother":        "👦",
    "Sister":         "👧",
    "Food":           "🍎",
    "Drink":          "🥤",
    "Stop":           "✋",
    "Go":             "🏃",
    "Come":           "👈",
    "Wait":           "⏳",
}


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">🤚 Gesture Recognition</div>
            <div class="page-subtitle">33 Common Signs · Instant Detection</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model = get_model()
    is_demo = model is None

    if is_demo:
        st.markdown(
            '<div style="text-align:center; margin-bottom:1rem">'
            '<span class="badge badge-cyan"><span class="badge-dot"></span>'
            'DEMO MODE</span></div>',
            unsafe_allow_html=True,
        )

    col_cam, col_result = st.columns([3, 2])

    with col_cam:
        st.markdown("<div class='section-header'>CAMERA FEED</div>", unsafe_allow_html=True)
        camera_input = st.camera_input(
            "Point your hand at the camera",
            key="gesture_cam",
            label_visibility="collapsed",
        )
        tts_controls()

    with col_result:
        st.markdown("<div class='section-header'>DETECTED GESTURE</div>", unsafe_allow_html=True)
        pred_placeholder = st.empty()
        conf_placeholder = st.empty()

        if camera_input is not None:
            img_bytes = camera_input.getvalue()
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is not None:
                if is_demo:
                    result = get_demo_prediction("gesture")
                else:
                    extractor = HandExtractor()
                    features = extractor.extract(frame)
                    if features is not None:
                        result = model.predict(features, GESTURE_LABELS)
                    else:
                        result = {"label": "No hand detected", "confidence": 0.0}

                label = result["label"]
                conf  = result["confidence"]
                emoji = GESTURE_EMOJIS.get(label, "🤚")

                if label not in ("—", "No hand detected"):
                    record_prediction(label, conf, mode="gesture")
                    speak_text(label)

                pred_placeholder.markdown(
                    f"""
                    <div class="prediction-box">
                        <div style="font-size:3.5rem">{emoji}</div>
                        <div class="prediction-word">{label}</div>
                        <div class="confidence-label">Detected Gesture</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                conf_color = "#00ff88" if conf >= 80 else "#ffd60a" if conf >= 60 else "#ff2d55"
                conf_placeholder.markdown(
                    f"""
                    <div style="margin-top:12px">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px">
                            <span style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted)">CONFIDENCE</span>
                            <span style="font-family:var(--font-head); font-size:1.1rem; font-weight:700; color:{conf_color}">{conf}%</span>
                        </div>
                        <div class="conf-bar-wrap">
                            <div class="conf-bar-fill" style="width:{min(conf,100)}%; background:linear-gradient(90deg, var(--blue), {conf_color})"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            pred_placeholder.markdown(
                """
                <div class="prediction-box" style="border-color: rgba(0,245,255,0.3)">
                    <div style="font-size:3.5rem; opacity:0.3">🤚</div>
                    <div class="prediction-word" style="color: rgba(0,255,136,0.3)">Waiting...</div>
                    <div class="confidence-label">Open camera to start</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Gesture Reference Grid ──────────────────────────────────────────────
    st.markdown("<div class='section-header'>SUPPORTED GESTURES</div>", unsafe_allow_html=True)

    cols = st.columns(6)
    for i, gesture in enumerate(GESTURE_LABELS):
        with cols[i % 6]:
            emoji = GESTURE_EMOJIS.get(gesture, "🤚")
            is_current = st.session_state.get("last_prediction") == gesture
            highlight = "border-color:var(--cyan); box-shadow:var(--glow-cyan);" if is_current else ""
            st.markdown(
                f"""
                <div class="sign-card" style="margin-bottom:8px; {highlight}">
                    <div class="sign-emoji">{emoji}</div>
                    <div style="font-family:var(--font-mono); font-size:0.6rem;
                                color:var(--text-muted); letter-spacing:0.5px">{gesture}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
