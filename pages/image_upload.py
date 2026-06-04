"""
Image Upload Page
Upload an image to predict the sign language gesture
SignSpeak AI
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io
from utils.model_loader import get_model, ALPHABET_LABELS, ALL_LABELS
from utils.hand_extractor import HandExtractor, preprocess_image
from utils.tts import speak_text, tts_controls
from utils.history_utils import record_prediction
from utils.demo_predictor import get_demo_prediction


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">🖼️ Image Upload</div>
            <div class="page-subtitle">Upload a Photo · Get Instant Prediction</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model = get_model()
    is_demo = model is None

    col_upload, col_result = st.columns([3, 2])

    with col_upload:
        st.markdown("<div class='section-header'>UPLOAD IMAGE</div>", unsafe_allow_html=True)
        uploaded = st.file_uploader(
            "Upload a sign language image",
            type=["jpg", "jpeg", "png", "webp", "bmp"],
            label_visibility="collapsed",
        )

        if uploaded:
            img = Image.open(uploaded).convert("RGB")
            st.image(img, use_container_width=True, caption="Uploaded Image")

        tts_controls()

    with col_result:
        st.markdown("<div class='section-header'>PREDICTION</div>", unsafe_allow_html=True)

        if uploaded:
            # Process
            img_bytes = uploaded.read() if hasattr(uploaded, "read") else uploaded.getvalue()
            # Re-read since we may have read above
            uploaded.seek(0)
            img_bytes = uploaded.read()

            with st.spinner("Analyzing sign..."):
                if is_demo:
                    result = get_demo_prediction("image")
                else:
                    frame = preprocess_image(img_bytes)
                    if frame is not None:
                        extractor = HandExtractor(max_hands=1)
                        features = extractor.extract(frame)
                        if features is not None:
                            result = model.predict(features, ALL_LABELS)
                        else:
                            result = {"label": "No hand detected", "confidence": 0.0}
                    else:
                        result = {"label": "Invalid image", "confidence": 0.0}

            label = result["label"]
            conf  = result["confidence"]

            if label not in ("No hand detected", "Invalid image"):
                record_prediction(label, conf, mode="image")

            # Display
            is_alphabet = len(label) == 1 and label.isalpha()
            display_cls = "prediction-letter" if is_alphabet else "prediction-word"
            conf_color = "#00ff88" if conf >= 80 else "#ffd60a" if conf >= 60 else "#ff2d55"

            st.markdown(
                f"""
                <div class="prediction-box">
                    <div class="{display_cls}">{label}</div>
                    <div class="confidence-label">Predicted Sign</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="margin-top:16px">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px">
                        <span style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted)">CONFIDENCE</span>
                        <span style="font-family:var(--font-head); font-size:1.2rem; font-weight:700; color:{conf_color}">{conf}%</span>
                    </div>
                    <div class="conf-bar-wrap" style="height:10px">
                        <div class="conf-bar-fill" style="width:{min(conf,100)}%;
                            background:linear-gradient(90deg, var(--blue), {conf_color})"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                if st.button("🔊 Speak", use_container_width=True):
                    speak_text(label)
            with c2:
                if st.button("➕ Add to Word", use_container_width=True):
                    if len(label) == 1:
                        st.session_state.current_letters.append(label)
                        st.session_state.current_word = "".join(st.session_state.current_letters)
                    else:
                        st.session_state.sentence_words.append(label)
                        st.session_state.full_sentence = " ".join(st.session_state.sentence_words)
                    st.success(f"Added '{label}' to builder!")

        else:
            st.markdown(
                """
                <div class="prediction-box" style="border-color:rgba(0,245,255,0.2)">
                    <div style="font-size:3rem; opacity:0.3; margin-bottom:8px">🖼️</div>
                    <div style="font-family:var(--font-mono); font-size:0.8rem; color:var(--text-muted)">
                        Upload an image to analyze
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Tips ──────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>TIPS FOR BEST RESULTS</div>", unsafe_allow_html=True)
    tips = [
        ("💡", "Good Lighting", "Ensure your hand is well-lit with no harsh shadows."),
        ("✋", "Clear Hand", "Keep only one hand visible, facing the camera directly."),
        ("📐", "Proper Angle", "Position hand at camera level, not from extreme angles."),
        ("🎨", "Plain Background", "Use a plain, contrasting background behind your hand."),
    ]

    tip_cols = st.columns(4)
    for i, (icon, title, desc) in enumerate(tips):
        with tip_cols[i]:
            st.markdown(
                f"""
                <div class="card" style="text-align:center; padding:1rem">
                    <div style="font-size:1.8rem; margin-bottom:8px">{icon}</div>
                    <div style="font-family:var(--font-head); font-size:0.9rem; font-weight:600;
                                color:var(--cyan); margin-bottom:4px">{title}</div>
                    <div style="font-family:var(--font-mono); font-size:0.65rem; color:var(--text-muted)">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
