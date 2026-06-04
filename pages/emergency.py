"""
Emergency Communication Mode Page
Large one-tap buttons for urgent communication
SignSpeak AI
"""

import streamlit as st
from utils.tts import speak_text


EMERGENCY_BUTTONS = [
    ("🆘", "HELP",        "Help me! I need assistance immediately!",   "#ff2d55"),
    ("👨‍⚕️", "DOCTOR",    "I need a doctor immediately!",               "#ff6b35"),
    ("🚔", "POLICE",      "Call the police! Emergency!",               "#ff2d55"),
    ("💧", "WATER",       "I need water, please.",                     "#0080ff"),
    ("🍎", "FOOD",        "I am hungry, I need food.",                 "#00c851"),
    ("📞", "CALL FAMILY", "Please call my family!",                   "#8b5cf6"),
    ("🏥", "HOSPITAL",    "Take me to the hospital now!",              "#ff2d55"),
    ("🔥", "FIRE",        "Fire! Emergency! Evacuate now!",            "#ff4500"),
    ("😣", "PAIN",        "I am in severe pain!",                     "#ff2d55"),
    ("💊", "MEDICINE",    "I need my medicine right now!",            "#0080ff"),
    ("🚗", "ACCIDENT",    "There has been an accident!",              "#ff6b35"),
    ("☎️", "CALL 112",    "Call emergency services, one-one-two!",    "#ff2d55"),
]


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">🆘 Emergency Mode</div>
            <div class="page-subtitle">One-Tap Emergency Communication</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Warning banner
    st.markdown(
        """
        <div style="background:linear-gradient(135deg, rgba(255,45,85,0.1), rgba(255,45,85,0.05));
                    border:2px solid rgba(255,45,85,0.5); border-radius:12px;
                    padding:1rem 1.5rem; text-align:center; margin-bottom:1.5rem">
            <div style="font-family:var(--font-head); font-size:1.1rem; font-weight:700;
                        color:#ff2d55; letter-spacing:2px">
                ⚡ EMERGENCY COMMUNICATION MODE
            </div>
            <div style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted); margin-top:4px">
                Tap any button to speak the emergency message aloud instantly
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Last spoken
    last = st.session_state.get("last_emergency_msg", "")
    if last:
        st.markdown(
            f"""
            <div style="background:rgba(255,45,85,0.08); border:1px solid rgba(255,45,85,0.3);
                        border-radius:10px; padding:12px 20px; margin-bottom:1rem; text-align:center">
                <div style="font-family:var(--font-mono); font-size:0.65rem; color:var(--text-muted)">LAST SPOKEN</div>
                <div style="font-family:var(--font-head); font-size:1.2rem; color:#ff2d55; margin-top:4px">{last}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Emergency Buttons Grid ─────────────────────────────────────────────
    cols = st.columns(3)
    for i, (icon, label, message, color) in enumerate(EMERGENCY_BUTTONS):
        with cols[i % 3]:
            # Inline CSS via container
            st.markdown(
                f"""
                <style>
                    div[data-testid="stButton"] button[kind="secondary"].emerg_{i} {{
                        background: linear-gradient(135deg, rgba(255,45,85,0.15), rgba(255,45,85,0.05)) !important;
                        border: 2px solid {color}88 !important;
                        color: {color} !important;
                        font-family: var(--font-head) !important;
                        font-size: 1rem !important;
                        font-weight: 700 !important;
                        letter-spacing: 2px !important;
                        padding: 16px !important;
                        border-radius: 12px !important;
                        min-height: 80px !important;
                    }}
                </style>
                """,
                unsafe_allow_html=True,
            )
            btn_label = f"{icon}\n{label}"
            if st.button(
                f"{icon}  {label}",
                key=f"emerg_{i}",
                use_container_width=True,
                help=message,
            ):
                speak_text(message)
                st.session_state.last_emergency_msg = message
                st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Custom Message ─────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>CUSTOM MESSAGE</div>", unsafe_allow_html=True)
    custom = st.text_area(
        "Type your emergency message",
        placeholder="Type your message here and click Speak...",
        key="emergency_custom",
        label_visibility="collapsed",
        height=80,
    )
    if st.button("🔊 SPEAK NOW", use_container_width=True):
        if custom:
            speak_text(custom)
            st.session_state.last_emergency_msg = custom
            st.rerun()

    # ── Important Contacts ─────────────────────────────────────────────────
    st.markdown("<div class='section-header'>EMERGENCY NUMBERS (INDIA)</div>", unsafe_allow_html=True)
    contacts = [
        ("🚔", "Police",         "100"),
        ("🚒", "Fire Brigade",   "101"),
        ("🚑", "Ambulance",      "102"),
        ("🆘", "Emergency",      "112"),
        ("👩", "Women Helpline", "1091"),
        ("🧒", "Child Helpline", "1098"),
    ]

    contact_cols = st.columns(6)
    for i, (icon, name, number) in enumerate(contacts):
        with contact_cols[i]:
            st.markdown(
                f"""
                <div class="card" style="text-align:center; padding:12px">
                    <div style="font-size:1.5rem">{icon}</div>
                    <div style="font-family:var(--font-head); font-size:1.3rem; font-weight:700;
                                color:var(--red, #ff2d55)">{number}</div>
                    <div style="font-family:var(--font-mono); font-size:0.6rem; color:var(--text-muted)">{name}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
