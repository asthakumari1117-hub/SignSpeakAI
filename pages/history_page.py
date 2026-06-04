"""
Prediction History Page
SignSpeak AI
"""

import streamlit as st
import pandas as pd
from utils.history_utils import load_history_df, export_csv, export_txt


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">📚 History</div>
            <div class="page-subtitle">Prediction Log · Download Your Data</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_history_df()

    if df.empty:
        st.markdown(
            """
            <div style="text-align:center; padding:4rem; color:var(--text-muted)">
                <div style="font-size:4rem; margin-bottom:1rem">📭</div>
                <div style="font-family:var(--font-head); font-size:1.5rem; color:var(--text-secondary)">
                    No Predictions Yet
                </div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; margin-top:8px">
                    Use Live Detection or Image Upload to start detecting signs
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Summary stats ─────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""<div class="metric-card metric-card-cyan">
                <div class="metric-val" style="color:var(--cyan)">{len(df)}</div>
                <div class="metric-lbl">Total Records</div>
            </div>""", unsafe_allow_html=True)
    with c2:
        avg = round(df["confidence"].mean(), 1)
        st.markdown(
            f"""<div class="metric-card metric-card-green">
                <div class="metric-val" style="color:var(--green)">{avg}%</div>
                <div class="metric-lbl">Avg Confidence</div>
            </div>""", unsafe_allow_html=True)
    with c3:
        top = df["sign"].value_counts().idxmax() if not df.empty else "—"
        st.markdown(
            f"""<div class="metric-card metric-card-blue">
                <div class="metric-val" style="color:var(--blue); font-size:1.8rem">{top}</div>
                <div class="metric-lbl">Most Detected</div>
            </div>""", unsafe_allow_html=True)
    with c4:
        unique = df["sign"].nunique()
        st.markdown(
            f"""<div class="metric-card metric-card-cyan">
                <div class="metric-val" style="color:var(--cyan)">{unique}</div>
                <div class="metric-lbl">Unique Signs</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Filters ───────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>FILTER</div>", unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        modes = ["All"] + sorted(df["mode"].unique().tolist()) if "mode" in df.columns else ["All"]
        mode_filter = st.selectbox("Mode", modes, key="hist_mode_filter")
    with fc2:
        min_conf = st.slider("Min Confidence %", 0, 100, 0, key="hist_conf_filter")
    with fc3:
        search = st.text_input("Search Sign", "", key="hist_search", placeholder="e.g. A or Hello")

    # Apply filters
    filtered = df.copy()
    if mode_filter != "All" and "mode" in filtered.columns:
        filtered = filtered[filtered["mode"] == mode_filter]
    filtered = filtered[filtered["confidence"] >= min_conf]
    if search:
        filtered = filtered[filtered["sign"].str.contains(search.upper(), case=False, na=False)]

    # ── History List ──────────────────────────────────────────────────────────
    st.markdown(
        f"<div class='section-header'>RECORDS <span style='color:var(--text-muted); font-size:0.7rem'>({len(filtered)} shown)</span></div>",
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No records match the current filters.")
    else:
        # Show as styled rows
        display_df = filtered.head(100)
        for _, row in display_df.iterrows():
            conf_color = "#00ff88" if row["confidence"] >= 80 else "#ffd60a" if row["confidence"] >= 60 else "#ff2d55"
            st.markdown(
                f"""
                <div class="history-row">
                    <span class="history-sign">{row['sign']}</span>
                    <span class="history-conf" style="color:{conf_color}">{row['confidence']}%</span>
                    <span style="color:var(--text-muted); font-size:0.7rem;
                                background:rgba(0,245,255,0.05); padding:2px 8px; border-radius:4px">
                        {row.get('mode','live')}
                    </span>
                    <span class="history-time">{row.get('date','')} {row['time']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>EXPORT</div>", unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)
    with e1:
        st.download_button(
            "📊 Download CSV",
            export_csv(filtered),
            file_name="signspeak_history.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with e2:
        st.download_button(
            "📄 Download TXT",
            export_txt(filtered),
            file_name="signspeak_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with e3:
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.prediction_history = []
            st.session_state.total_predictions  = 0
            st.session_state.sign_counts        = {}
            st.rerun()
