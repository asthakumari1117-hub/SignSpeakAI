"""
Settings & Accessibility Page
SignSpeak AI
"""

import streamlit as st


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">⚙️ Settings</div>
            <div class="page-subtitle">Customize · Accessibility · Preferences</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["🔊 Audio", "♿ Accessibility", "🤖 Model Info"])

    # ── Tab 1: Audio ──────────────────────────────────────────────────────────
    with tab1:
        st.markdown("<div class='section-header'>TEXT-TO-SPEECH</div>", unsafe_allow_html=True)

        tts_enabled = st.toggle(
            "Enable Voice Output (TTS)",
            value=st.session_state.get("tts_enabled", True),
            key="settings_tts_toggle",
        )
        st.session_state.tts_enabled = tts_enabled

        engine = st.radio(
            "TTS Engine",
            ["gtts", "pyttsx3"],
            index=0 if st.session_state.get("tts_engine", "gtts") == "gtts" else 1,
            horizontal=True,
            help="gTTS requires internet. pyttsx3 works offline but may not work on Streamlit Cloud.",
        )
        st.session_state.tts_engine = engine

        st.markdown(
            """
            <div class="card" style="margin-top:12px">
                <div style="font-family:var(--font-head); font-size:0.9rem; color:var(--cyan); margin-bottom:8px">
                    🔊 Engine Info
                </div>
                <div style="font-family:var(--font-mono); font-size:0.72rem; color:var(--text-secondary); line-height:1.6">
                    <strong style="color:var(--green)">gTTS (Google TTS)</strong> — Cloud-based, natural voice, requires internet.<br>
                    Best for Streamlit Cloud deployments.<br><br>
                    <strong style="color:var(--blue)">pyttsx3</strong> — Offline, system voice, no internet needed.<br>
                    Best for local/Windows deployments.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='section-header'>DEFAULT LANGUAGE</div>", unsafe_allow_html=True)
        from utils.translator import SUPPORTED_LANGUAGES
        langs = list(SUPPORTED_LANGUAGES.keys())
        current_lang = st.session_state.get("output_language", "English")
        selected = st.selectbox(
            "Default Output Language",
            langs,
            index=langs.index(current_lang) if current_lang in langs else 0,
        )
        st.session_state.output_language = selected

    # ── Tab 2: Accessibility ──────────────────────────────────────────────────
    with tab2:
        st.markdown("<div class='section-header'>ACCESSIBILITY OPTIONS</div>", unsafe_allow_html=True)

        large_text = st.toggle(
            "Large Text Mode",
            value=st.session_state.get("large_text", False),
            help="Increases text and prediction display size",
        )
        st.session_state.large_text = large_text

        high_contrast = st.toggle(
            "High Contrast Mode",
            value=st.session_state.get("high_contrast", False),
            help="Increases color contrast for better visibility",
        )
        st.session_state.high_contrast = high_contrast

        voice_feedback = st.toggle(
            "Voice Feedback on Every Detection",
            value=st.session_state.get("voice_feedback", False),
            help="Speaks every detected sign automatically",
        )
        st.session_state.voice_feedback = voice_feedback

        # Apply CSS modifiers
        if large_text:
            st.markdown(
                """<style>
                .prediction-letter { font-size: 8rem !important; }
                .prediction-word   { font-size: 3.5rem !important; }
                .word-display      { font-size: 3rem !important; }
                .sentence-display  { font-size: 1.8rem !important; }
                body, .stApp       { font-size: 1.1rem !important; }
                </style>""",
                unsafe_allow_html=True,
            )

        if high_contrast:
            st.markdown(
                """<style>
                :root {
                    --text-primary:   #ffffff !important;
                    --text-secondary: #d0e8ff !important;
                    --bg-card:        #081020 !important;
                    --border:         rgba(0,245,255,0.5) !important;
                }
                </style>""",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="card" style="margin-top:12px">
                <div style="font-family:var(--font-head); font-size:0.9rem; color:var(--cyan); margin-bottom:8px">
                    ♿ About Accessibility
                </div>
                <div style="font-family:var(--font-mono); font-size:0.72rem; color:var(--text-secondary); line-height:1.6">
                    SignSpeak AI is designed to be fully accessible for users with visual,
                    motor, and hearing impairments. Features include large text mode,
                    high contrast, voice output, and one-tap emergency communication.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Tab 3: Model Info ─────────────────────────────────────────────────────
    with tab3:
        st.markdown("<div class='section-header'>MODEL CONFIGURATION</div>", unsafe_allow_html=True)

        from utils.model_loader import find_model, get_model, MODEL_EXTENSIONS
        import os

        model_path = find_model()

        if model_path:
            model = get_model()
            size = os.path.getsize(model_path) / 1024
            st.markdown(
                f"""
                <div class="card card-green">
                    <div class="badge badge-green" style="margin-bottom:12px">
                        <span class="badge-dot"></span> MODEL LOADED
                    </div>
                    <table style="font-family:var(--font-mono); font-size:0.78rem; width:100%; border-collapse:collapse">
                        <tr>
                            <td style="color:var(--text-muted); padding:4px 0">Path</td>
                            <td style="color:var(--text-primary)">{model_path}</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); padding:4px 0">Type</td>
                            <td style="color:var(--cyan)">{model.model_type.upper() if model else '—'}</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); padding:4px 0">Size</td>
                            <td style="color:var(--text-primary)">{size:.1f} KB</td>
                        </tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="card card-cyan">
                    <div class="badge badge-cyan" style="margin-bottom:12px">
                        <span class="badge-dot"></span> DEMO MODE
                    </div>
                    <div style="font-family:var(--font-mono); font-size:0.78rem; color:var(--text-secondary); line-height:1.6">
                        No model file found in <code>models/</code> directory.<br>
                        The app is running in demo mode with simulated predictions.<br><br>
                        To enable real predictions, place your pre-trained model in:<br>
                        <code style="color:var(--cyan)">models/sign_model.pkl</code> — for scikit-learn models<br>
                        <code style="color:var(--cyan)">models/sign_model.h5</code>  — for Keras/TF models<br>
                        <code style="color:var(--cyan)">models/sign_model.tflite</code> — for TFLite models<br>
                        <code style="color:var(--cyan)">models/sign_model.pt</code>  — for PyTorch models
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<div class='section-header'>SUPPORTED FORMATS</div>", unsafe_allow_html=True)
        for ext in MODEL_EXTENSIONS:
            label_map = {
                ".pkl": "scikit-learn / Any Pickle", ".pickle": "scikit-learn / Any Pickle",
                ".h5": "TensorFlow / Keras", ".keras": "TensorFlow / Keras",
                ".tflite": "TensorFlow Lite (mobile-optimized)",
                ".pt": "PyTorch", ".pth": "PyTorch",
            }
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:12px; padding:6px 0;
                            border-bottom:1px solid var(--border)">
                    <code style="color:var(--cyan); font-size:0.85rem; min-width:80px">{ext}</code>
                    <span style="font-family:var(--font-mono); font-size:0.72rem; color:var(--text-secondary)">
                        {label_map.get(ext, ext)}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Session reset
        st.markdown("<div class='section-header'>SESSION</div>", unsafe_allow_html=True)
        if st.button("🔄 Reset All Session Data", use_container_width=True):
            for key in ["prediction_history", "current_letters", "sentence_words",
                        "full_sentence", "current_word", "sign_counts",
                        "total_predictions", "last_prediction"]:
                if key in st.session_state:
                    del st.session_state[key]
            from utils.session import init_session_state
            init_session_state()
            st.success("✅ Session reset successfully!")
            st.rerun()
