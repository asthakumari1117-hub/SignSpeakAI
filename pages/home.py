"""
Home Page - SignSpeak AI
"""

import streamlit as st
from utils.model_loader import get_model, find_model


def render():
    # Hero
    st.markdown(
        """
        <div class="hero-section fade-in-up">
            <div style="font-size:4rem; margin-bottom:12px; filter:drop-shadow(0 0 16px rgba(0,245,255,0.6))">🤟</div>
            <div class="hero-title">SignSpeak AI</div>
            <div class="hero-tagline">AI-Powered Sign Language Translator · Final Year Project</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Model status
    model_path = find_model()
    if model_path:
        model = get_model()
        status_html = f"""
        <div style="text-align:center; margin-bottom:2rem;">
            <span class="badge badge-green"><span class="badge-dot"></span>MODEL LOADED · {model_path}</span>
        </div>"""
    else:
        status_html = """
        <div style="text-align:center; margin-bottom:2rem;">
            <span class="badge badge-cyan"><span class="badge-dot"></span>DEMO MODE · Place your model in models/ folder</span>
        </div>"""
    st.markdown(status_html, unsafe_allow_html=True)

    # Feature grid
    features = [
        ("📷", "Live Detection",      "Real-time webcam sign detection with instant A-Z recognition",                "live_detection", "cyan"),
        ("🤚", "Gesture Recognition", "Detect 33 common gestures: Hello, Thank You, I Love You, and more",           "gesture",       "blue"),
        ("🔤", "Word Builder",        "Spell words letter-by-letter and build complete sentences",                   "word_builder",  "green"),
        ("🖼️", "Image Upload",        "Upload any photo and get instant sign language prediction",                   "image_upload",  "cyan"),
        ("🌐", "Multi-Language",      "Translate detected text into Hindi, French, Spanish, German, Arabic & more", "multi_language","blue"),
        ("🆘", "Emergency Mode",       "One-tap emergency communication for HELP, DOCTOR, POLICE & more",            "emergency",     "green"),
        ("📊", "Statistics",          "Track your usage patterns, top signs, confidence scores & more",             "statistics",    "cyan"),
        ("🎓", "Learning Mode",       "Visual alphabet & gesture guide to learn sign language",                     "learning",      "blue"),
    ]

    cols = st.columns(2)
    for i, (icon, title, desc, page, color) in enumerate(features):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="card card-{color}" style="margin-bottom:12px; cursor:pointer;">
                    <div style="display:flex; align-items:flex-start; gap:14px;">
                        <div style="font-size:2rem; filter:drop-shadow(0 0 6px rgba(0,245,255,0.5))">{icon}</div>
                        <div>
                            <div style="font-family:var(--font-head); font-size:1.1rem; font-weight:700;
                                        color:var(--text-primary); letter-spacing:1px; margin-bottom:4px">{title}</div>
                            <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted);
                                        line-height:1.4">{desc}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open {title}", key=f"home_btn_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()

    # Quick Stats
    st.markdown("<div class='section-header'>SESSION STATS</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="metric-card metric-card-cyan">
                <div class="metric-val" style="color:var(--cyan)">{st.session_state.get('total_predictions', 0)}</div>
                <div class="metric-lbl">Total Predictions</div>
            </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(
            f"""<div class="metric-card metric-card-green">
                <div class="metric-val" style="color:var(--green)">{len(st.session_state.get('sentence_words', []))}</div>
                <div class="metric-lbl">Words Built</div>
            </div>""", unsafe_allow_html=True)
    with c3:
        hist = st.session_state.get("prediction_history", [])
        avg = round(sum(h["confidence"] for h in hist) / max(len(hist), 1), 1) if hist else 0
        st.markdown(
            f"""<div class="metric-card metric-card-blue">
                <div class="metric-val" style="color:var(--blue)">{avg}%</div>
                <div class="metric-lbl">Avg Confidence</div>
            </div>""", unsafe_allow_html=True)
    with c4:
        counts = st.session_state.get("sign_counts", {})
        top = max(counts, key=counts.get) if counts else "—"
        st.markdown(
            f"""<div class="metric-card metric-card-cyan">
                <div class="metric-val" style="color:var(--cyan); font-size:1.8rem">{top}</div>
                <div class="metric-lbl">Top Sign</div>
            </div>""", unsafe_allow_html=True)

    # About
    st.markdown("<div class='section-header'>ABOUT THIS PROJECT</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card" style="margin-top:8px">
            <p style="font-family:var(--font-main); color:var(--text-secondary); line-height:1.7; font-size:0.9rem">
                <strong style="color:var(--cyan)">SignSpeak AI</strong> is a final-year AI project that bridges the communication gap
                between the deaf/mute community and the general public. Using advanced computer vision (MediaPipe) and
                machine learning, the system detects hand signs in real-time and converts them into text and speech.
            </p>
            <p style="font-family:var(--font-main); color:var(--text-secondary); line-height:1.7; font-size:0.9rem">
                The application supports <strong style="color:var(--green)">A-Z alphabet detection</strong>,
                <strong style="color:var(--green)">33 common gestures</strong>, word and sentence building,
                multi-language translation, emergency communication, and more.
            </p>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:12px">
                <span class="badge badge-cyan">Python 3.10+</span>
                <span class="badge badge-cyan">MediaPipe</span>
                <span class="badge badge-cyan">Streamlit</span>
                <span class="badge badge-green">OpenCV</span>
                <span class="badge badge-green">scikit-learn</span>
                <span class="badge badge-green">TensorFlow</span>
                <span class="badge badge-cyan">gTTS</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
