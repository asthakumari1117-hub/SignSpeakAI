"""
Multi-Language Translation Page
Translate sign language output to multiple languages
SignSpeak AI
"""

import streamlit as st
from utils.translator import translate_text, SUPPORTED_LANGUAGES
from utils.tts import speak_text, tts_controls, get_gtts_lang_code


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">🌐 Multi-Language</div>
            <div class="page-subtitle">Translate Sign Language Output · 7 Languages</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Language cards
    lang_info = {
        "English":  ("🇬🇧", "en"),
        "Hindi":    ("🇮🇳", "hi"),
        "Punjabi":  ("🇮🇳", "pa"),
        "French":   ("🇫🇷", "fr"),
        "Spanish":  ("🇪🇸", "es"),
        "German":   ("🇩🇪", "de"),
        "Arabic":   ("🇸🇦", "ar"),
    }

    # Language selector
    st.markdown("<div class='section-header'>SELECT TARGET LANGUAGE</div>", unsafe_allow_html=True)
    lang_cols = st.columns(7)
    current_lang = st.session_state.get("output_language", "English")

    for i, (lang, (flag, code)) in enumerate(lang_info.items()):
        with lang_cols[i]:
            is_active = current_lang == lang
            border = "border-color:var(--cyan); box-shadow:var(--glow-cyan);" if is_active else ""
            text_color = "color:var(--cyan);" if is_active else ""
            st.markdown(
                f"""
                <div class="sign-card" style="{border} margin-bottom:8px; padding:10px">
                    <div style="font-size:1.8rem">{flag}</div>
                    <div style="font-family:var(--font-mono); font-size:0.6rem;
                                {text_color} margin-top:4px">{lang}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(lang[:3], key=f"lang_btn_{lang}", use_container_width=True):
                st.session_state.output_language = lang
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Translation input
    col_in, col_out = st.columns(2)

    with col_in:
        st.markdown("<div class='section-header'>INPUT (ENGLISH)</div>", unsafe_allow_html=True)

        # Pre-fill from session sentence if available
        session_sentence = st.session_state.get("full_sentence", "")
        default_text = session_sentence if session_sentence else ""

        input_text = st.text_area(
            "Enter text to translate",
            value=default_text,
            placeholder="Type or detect a sign language message...",
            height=150,
            key="translate_input",
            label_visibility="collapsed",
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔊 Speak English", use_container_width=True):
                speak_text(input_text, lang="en")
        with c2:
            if st.button("📋 Use Session Sentence", use_container_width=True):
                if session_sentence:
                    st.rerun()

    with col_out:
        target_lang = st.session_state.get("output_language", "English")
        flag, lang_code = lang_info.get(target_lang, ("🌐", "en"))
        st.markdown(f"<div class='section-header'>OUTPUT ({target_lang.upper()} {flag})</div>", unsafe_allow_html=True)

        if input_text and input_text.strip():
            with st.spinner(f"Translating to {target_lang}..."):
                translated = translate_text(input_text, target_lang)
                st.session_state.translated_text = translated

            direction = "rtl" if target_lang == "Arabic" else "ltr"
            st.markdown(
                f"""
                <div class="sentence-display" style="direction:{direction}; min-height:120px;
                            display:flex; align-items:center; justify-content:center;">
                    {translated}
                </div>
                """,
                unsafe_allow_html=True,
            )

            c1, c2 = st.columns(2)
            with c1:
                gtts_code = get_gtts_lang_code(target_lang)
                if st.button(f"🔊 Speak {target_lang}", use_container_width=True):
                    speak_text(translated, lang=gtts_code)
            with c2:
                st.download_button(
                    "📥 Download TXT",
                    f"Original ({input_text})\n{target_lang} ({translated})",
                    file_name=f"translation_{lang_code}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
        else:
            st.markdown(
                """
                <div class="sentence-display" style="min-height:120px; display:flex;
                            align-items:center; justify-content:center;
                            color:var(--text-muted); font-size:0.8rem">
                    Translation will appear here
                </div>
                """,
                unsafe_allow_html=True,
            )

    tts_controls()

    # ── All translations ───────────────────────────────────────────────────
    if input_text and input_text.strip():
        st.markdown("<div class='section-header'>ALL TRANSLATIONS</div>", unsafe_allow_html=True)

        all_cols = st.columns(2)
        for i, (lang, (flag, code)) in enumerate(lang_info.items()):
            with all_cols[i % 2]:
                with st.spinner(f"Translating to {lang}..."):
                    result = translate_text(input_text, lang)
                direction = "rtl" if lang == "Arabic" else "ltr"
                st.markdown(
                    f"""
                    <div class="card" style="margin-bottom:8px; padding:12px 16px">
                        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px">
                            <span style="font-size:1.2rem">{flag}</span>
                            <span style="font-family:var(--font-head); font-size:0.9rem;
                                        color:var(--cyan); font-weight:600">{lang}</span>
                        </div>
                        <div style="font-family:var(--font-main); color:var(--text-primary);
                                    direction:{direction}; font-size:0.95rem">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
