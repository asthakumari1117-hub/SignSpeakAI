"""
Word & Sentence Builder Page
SignSpeak AI
"""

import streamlit as st
from utils.tts import speak_text, tts_controls
from utils.history_utils import record_prediction
from utils.model_loader import ALPHABET_LABELS


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">🔤 Word Builder</div>
            <div class="page-subtitle">Build Words and Sentences from Signs</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tts_controls()

    # ── Manual Input Section ──────────────────────────────────────────────────
    st.markdown("<div class='section-header'>MANUAL SIGN INPUT</div>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted);">'
        "Click letters to add them, or use Live Detection page for real camera input.</p>",
        unsafe_allow_html=True,
    )

    # Alphabet keyboard
    rows = [
        list("ABCDEFGHIJ"),
        list("KLMNOPQRST"),
        list("UVWXYZ"),
    ]

    for row in rows:
        cols = st.columns(len(row))
        for i, letter in enumerate(row):
            with cols[i]:
                if st.button(letter, key=f"kb_{letter}", use_container_width=True):
                    st.session_state.current_letters.append(letter)
                    st.session_state.current_word = "".join(st.session_state.current_letters)
                    record_prediction(letter, 100.0, mode="manual")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Current Word ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>CURRENT WORD</div>", unsafe_allow_html=True)

    letters = st.session_state.get("current_letters", [])
    if letters:
        chips_html = "".join(f'<span class="letter-chip">{l}</span>' for l in letters)
        st.markdown(f'<div class="letter-chips">{chips_html}</div>', unsafe_allow_html=True)
        word = "".join(letters)
        st.markdown(f'<div class="word-display" style="font-size:2.5rem">{word}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="text-align:center; color:var(--text-muted); font-family:var(--font-mono); '
            'font-size:0.8rem; padding:20px; border:1px dashed rgba(0,245,255,0.2); border-radius:10px">'
            'No letters yet — click keyboard above or use Live Detection</div>',
            unsafe_allow_html=True,
        )

    # Word actions
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅️ Backspace", use_container_width=True):
            if st.session_state.current_letters:
                st.session_state.current_letters.pop()
                st.session_state.current_word = "".join(st.session_state.current_letters)
                st.rerun()
    with c2:
        if st.button("🗑️ Clear Word", use_container_width=True):
            st.session_state.current_letters = []
            st.session_state.current_word = ""
            st.rerun()
    with c3:
        if st.button("✅ Add to Sentence", use_container_width=True):
            word = st.session_state.current_word
            if word:
                st.session_state.sentence_words.append(word)
                st.session_state.full_sentence = " ".join(st.session_state.sentence_words)
                st.session_state.current_letters = []
                st.session_state.current_word = ""
                speak_text(word)
                st.rerun()
    with c4:
        if st.button("🔊 Speak Word", use_container_width=True):
            speak_text(st.session_state.current_word)

    # ── Sentence Builder ──────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>SENTENCE BUILDER</div>", unsafe_allow_html=True)

    sentence_words = st.session_state.get("sentence_words", [])
    if sentence_words:
        # Word chips
        word_chips = "".join(
            f'<span class="letter-chip" style="background:rgba(0,128,255,0.1); '
            f'border-color:rgba(0,128,255,0.5); color:var(--blue)">{w}</span>'
            for w in sentence_words
        )
        st.markdown(f'<div class="letter-chips">{word_chips}</div>', unsafe_allow_html=True)

        # Full sentence
        sentence = " ".join(sentence_words)
        st.markdown(f'<div class="sentence-display">{sentence}</div>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("🔊 Speak All", use_container_width=True):
                speak_text(sentence)
        with c2:
            if st.button("⬅️ Remove Last Word", use_container_width=True):
                st.session_state.sentence_words.pop()
                st.session_state.full_sentence = " ".join(st.session_state.sentence_words)
                st.rerun()
        with c3:
            if st.button("🗑️ Clear Sentence", use_container_width=True):
                st.session_state.sentence_words = []
                st.session_state.full_sentence = ""
                st.rerun()
        with c4:
            st.download_button(
                "📥 Save TXT",
                sentence,
                file_name="sentence.txt",
                mime="text/plain",
                use_container_width=True,
            )
    else:
        st.markdown(
            '<div style="text-align:center; color:var(--text-muted); font-family:var(--font-mono); '
            'font-size:0.8rem; padding:20px; border:1px dashed rgba(0,128,255,0.2); border-radius:10px">'
            'Add words to build a sentence</div>',
            unsafe_allow_html=True,
        )

    # ── Quick Phrases ─────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>QUICK PHRASES</div>", unsafe_allow_html=True)

    quick_phrases = [
        "HELLO",
        "THANK YOU",
        "HOW ARE YOU",
        "I AM FINE",
        "NICE TO MEET YOU",
        "HELP ME PLEASE",
        "I NEED WATER",
        "CALL DOCTOR",
    ]

    phrase_cols = st.columns(4)
    for i, phrase in enumerate(quick_phrases):
        with phrase_cols[i % 4]:
            if st.button(phrase, key=f"qp_{i}", use_container_width=True):
                st.session_state.sentence_words = phrase.split()
                st.session_state.full_sentence = phrase
                speak_text(phrase)
                st.rerun()
