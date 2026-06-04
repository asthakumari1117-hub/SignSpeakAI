"""
Learning Mode Page
Visual sign language guide with alphabet and gesture cards
SignSpeak AI
"""

import streamlit as st
from utils.model_loader import ALPHABET_LABELS, GESTURE_LABELS
from pages.gesture_recognition import GESTURE_EMOJIS

# Finger spelling hints for each letter
LETTER_HINTS = {
    "A": "Closed fist, thumb on side",
    "B": "Four fingers up, thumb tucked",
    "C": "Curved hand like a 'C'",
    "D": "Index up, others curved, thumb touches middle",
    "E": "All fingers curled, thumb tucked under",
    "F": "Index & thumb circle, others up",
    "G": "Index & thumb point sideways",
    "H": "Index & middle point sideways",
    "I": "Pinky up, others closed",
    "J": "Pinky up, draw J shape",
    "K": "Index & middle up, thumb between",
    "L": "Index up, thumb out = L shape",
    "M": "Three fingers over thumb",
    "N": "Two fingers over thumb",
    "O": "All fingers curved to form O",
    "P": "Like K but angled down",
    "Q": "Like G but angled down",
    "R": "Index & middle crossed",
    "S": "Fist, thumb over fingers",
    "T": "Fist, thumb between index & middle",
    "U": "Index & middle together, pointing up",
    "V": "Index & middle spread, V shape",
    "W": "Three fingers spread, W shape",
    "X": "Index finger hooked",
    "Y": "Pinky & thumb out",
    "Z": "Index draws Z in air",
}

LETTER_EMOJIS = {l: "🤚" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
LETTER_EMOJIS.update({
    "A": "✊", "B": "🖐️", "C": "🤏", "D": "👆",
    "E": "🤜", "F": "👌", "G": "👈", "H": "✌️",
    "I": "🤙", "J": "🤙", "K": "✌️", "L": "🤙",
    "M": "✊", "N": "✊", "O": "👌", "P": "👇",
    "Q": "👇", "R": "🤞", "S": "✊", "T": "✊",
    "U": "✌️", "V": "✌️", "W": "🖖", "X": "☝️",
    "Y": "🤙", "Z": "☝️",
})


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">🎓 Learning Mode</div>
            <div class="page-subtitle">Sign Language Reference Guide</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["🔤 Alphabet (A-Z)", "🤚 Common Gestures", "📖 Quick Reference"])

    # ── Tab 1: Alphabet ───────────────────────────────────────────────────────
    with tab1:
        st.markdown("<div class='section-header'>ASL FINGER SPELLING A–Z</div>", unsafe_allow_html=True)
        st.markdown(
            '<p style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted);">'
            "Click a card to hear the letter spoken aloud.</p>",
            unsafe_allow_html=True,
        )

        rows_of_5 = [ALPHABET_LABELS[i:i+5] for i in range(0, 26, 5)]
        for row in rows_of_5:
            cols = st.columns(5)
            for j, letter in enumerate(row):
                with cols[j]:
                    hint = LETTER_HINTS.get(letter, "")
                    emoji = LETTER_EMOJIS.get(letter, "🤚")
                    st.markdown(
                        f"""
                        <div class="sign-card" style="margin-bottom:10px; padding:1rem">
                            <div class="sign-letter">{letter}</div>
                            <div class="sign-emoji">{emoji}</div>
                            <div class="sign-desc" style="font-size:0.58rem; line-height:1.3">{hint}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    if st.button(f"🔊 {letter}", key=f"learn_letter_{letter}", use_container_width=True):
                        from utils.tts import speak_text
                        speak_text(letter)

    # ── Tab 2: Gestures ───────────────────────────────────────────────────────
    with tab2:
        st.markdown("<div class='section-header'>COMMON GESTURES & SIGNS</div>", unsafe_allow_html=True)

        cols = st.columns(4)
        for i, gesture in enumerate(GESTURE_LABELS):
            with cols[i % 4]:
                emoji = GESTURE_EMOJIS.get(gesture, "🤚")
                st.markdown(
                    f"""
                    <div class="sign-card" style="margin-bottom:10px">
                        <div style="font-size:2.5rem">{emoji}</div>
                        <div style="font-family:var(--font-head); font-size:0.85rem; font-weight:600;
                                    color:var(--cyan); margin:6px 0 2px 0">{gesture}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"🔊", key=f"learn_gesture_{i}", use_container_width=True):
                    from utils.tts import speak_text
                    speak_text(gesture)

    # ── Tab 3: Quick Reference ────────────────────────────────────────────────
    with tab3:
        st.markdown("<div class='section-header'>HANDSHAPE GUIDE</div>", unsafe_allow_html=True)

        tips_data = [
            ("👋", "Greeting Signs",  "HELLO, WELCOME, BYE — Open palm wave, direction & motion matter"),
            ("🙏", "Polite Signs",    "PLEASE, SORRY, THANK YOU — Both hands often involved"),
            ("✅", "Yes / No",        "YES: fist nod | NO: index & middle tap thumb"),
            ("🆘", "Emergency",       "HELP: flat hand on fist, lifting upward motion"),
            ("❤️", "Emotions",        "I LOVE YOU: pinky, index, thumb extended simultaneously"),
            ("🍽️", "Daily Needs",     "HUNGRY, WATER, FOOD — Natural mime-like gestures"),
            ("👨‍👩‍👧", "Family Signs",    "MOTHER: thumb on chin | FATHER: thumb on forehead"),
            ("🚦", "Direction Signs", "STOP, GO, COME, WAIT — Clear directional movements"),
        ]

        ref_cols = st.columns(2)
        for i, (icon, title, desc) in enumerate(tips_data):
            with ref_cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="card" style="margin-bottom:10px">
                        <div style="display:flex; gap:12px; align-items:flex-start">
                            <div style="font-size:2rem">{icon}</div>
                            <div>
                                <div style="font-family:var(--font-head); font-size:1rem; font-weight:600;
                                            color:var(--cyan); margin-bottom:4px">{title}</div>
                                <div style="font-family:var(--font-mono); font-size:0.7rem;
                                            color:var(--text-secondary); line-height:1.4">{desc}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Practice mode
        st.markdown("<div class='section-header'>PRACTICE QUIZ</div>", unsafe_allow_html=True)
        import random
        if "quiz_letter" not in st.session_state:
            st.session_state.quiz_letter = random.choice(ALPHABET_LABELS)

        quiz_letter = st.session_state.quiz_letter
        hint = LETTER_HINTS.get(quiz_letter, "")
        emoji = LETTER_EMOJIS.get(quiz_letter, "🤚")

        st.markdown(
            f"""
            <div class="prediction-box" style="max-width:300px; margin:0 auto">
                <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-muted); margin-bottom:8px">
                    SHOW THIS SIGN:
                </div>
                <div class="prediction-letter">{quiz_letter}</div>
                <div style="font-size:2rem; margin:8px 0">{emoji}</div>
                <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--text-secondary);
                            max-width:200px; margin:0 auto; line-height:1.4">{hint}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🔀 Next Letter", use_container_width=True):
            st.session_state.quiz_letter = random.choice(ALPHABET_LABELS)
            st.rerun()
