"""
SignSpeak AI - Main Application Entry Point
Final Year Project - AI Sign Language Translator
"""

import streamlit as st
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page config MUST be first Streamlit call
st.set_page_config(
    page_title="SignSpeak AI",
    page_icon="🤟",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/your-repo/SignSpeakAI",
        "Report a bug": "https://github.com/your-repo/SignSpeakAI/issues",
        "About": "# SignSpeak AI\nAI-Powered Sign Language Translator - Final Year Project",
    },
)

from utils.styles import inject_global_css
from utils.session import init_session_state

# Inject global CSS
inject_global_css()

# Initialize session state
init_session_state()

# Import page modules
from pages import (
    home,
    live_detection,
    gesture_recognition,
    word_builder,
    image_upload,
    history_page,
    statistics,
    learning_mode,
    emergency,
    settings,
    multi_language,
)

# ─── Sidebar Navigation ───────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo & Title
        st.markdown(
            """
            <div class="sidebar-logo">
                <div class="logo-icon">🤟</div>
                <div class="logo-text">
                    <span class="logo-main">SignSpeak</span>
                    <span class="logo-sub">AI Translator</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Home", "home"),
            ("📷", "Live Detection", "live_detection"),
            ("🤚", "Gesture Recognition", "gesture"),
            ("🔤", "Word Builder", "word_builder"),
            ("🖼️", "Image Upload", "image_upload"),
            ("📚", "History", "history"),
            ("📊", "Statistics", "statistics"),
            ("🎓", "Learning Mode", "learning"),
            ("🆘", "Emergency Mode", "emergency"),
            ("🌐", "Multi-Language", "multi_language"),
            ("⚙️", "Settings", "settings"),
        ]

        st.markdown("<p class='nav-label'>NAVIGATION</p>", unsafe_allow_html=True)

        for icon, label, page_key in nav_items:
            is_active = st.session_state.get("current_page", "home") == page_key
            btn_class = "nav-btn-active" if is_active else "nav-btn"
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{page_key}",
                use_container_width=True,
            ):
                st.session_state.current_page = page_key
                st.rerun()

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        # Quick Stats in Sidebar
        total = st.session_state.get("total_predictions", 0)
        st.markdown(
            f"""
            <div class="sidebar-stats">
                <div class="stat-item">
                    <span class="stat-val">{total}</span>
                    <span class="stat-lbl">Predictions</span>
                </div>
                <div class="stat-item">
                    <span class="stat-val">{len(st.session_state.get('sentence_words', []))}</span>
                    <span class="stat-lbl">Words Built</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="sidebar-footer">
                <p>SignSpeak AI v1.0</p>
                <p>Final Year Project</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ─── Main Router ──────────────────────────────────────────────────────────────
def main():
    render_sidebar()

    page = st.session_state.get("current_page", "home")

    page_map = {
        "home": home.render,
        "live_detection": live_detection.render,
        "gesture": gesture_recognition.render,
        "word_builder": word_builder.render,
        "image_upload": image_upload.render,
        "history": history_page.render,
        "statistics": statistics.render,
        "learning": learning_mode.render,
        "emergency": emergency.render,
        "multi_language": multi_language.render,
        "settings": settings.render,
    }

    render_fn = page_map.get(page, home.render)
    render_fn()


if __name__ == "__main__":
    main()
