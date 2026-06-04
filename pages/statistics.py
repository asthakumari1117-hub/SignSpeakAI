"""
Statistics Dashboard Page
SignSpeak AI
"""

import streamlit as st
import pandas as pd
from utils.history_utils import get_stats, load_history_df


def render():
    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">📊 Statistics</div>
            <div class="page-subtitle">Usage Analytics · Confidence Trends</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stats = get_stats()

    if stats["total"] == 0:
        st.markdown(
            """
            <div style="text-align:center; padding:4rem; color:var(--text-muted)">
                <div style="font-size:4rem; margin-bottom:1rem">📈</div>
                <div style="font-family:var(--font-head); font-size:1.5rem; color:var(--text-secondary)">
                    No Data Yet
                </div>
                <div style="font-family:var(--font-mono); font-size:0.75rem; margin-top:8px">
                    Start detecting signs to see your statistics
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # ── Top metrics ───────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("🎯 Total Predictions", stats["total"])
    with c2:
        st.metric("📈 Avg Confidence", f"{stats['avg_conf']}%")
    with c3:
        top_sign = stats["top_signs"][0][0] if stats["top_signs"] else "—"
        st.metric("🏆 Most Used Sign", top_sign)
    with c4:
        df = stats.get("df", pd.DataFrame())
        unique = df["sign"].nunique() if not df.empty else 0
        st.metric("🔤 Unique Signs", unique)

    # ── Charts ────────────────────────────────────────────────────────────────
    df = stats.get("df", pd.DataFrame())

    if not df.empty:
        tab1, tab2, tab3 = st.tabs(["📊 Sign Distribution", "📈 Confidence Over Time", "🎯 Mode Breakdown"])

        with tab1:
            st.markdown("<div class='section-header'>TOP SIGNS USED</div>", unsafe_allow_html=True)
            if stats["top_signs"]:
                top_df = pd.DataFrame(stats["top_signs"], columns=["Sign", "Count"])
                st.bar_chart(top_df.set_index("Sign")["Count"])

        with tab2:
            st.markdown("<div class='section-header'>CONFIDENCE TREND</div>", unsafe_allow_html=True)
            if "confidence" in df.columns:
                conf_series = df["confidence"].reset_index(drop=True)
                st.line_chart(conf_series)

        with tab3:
            st.markdown("<div class='section-header'>PREDICTION MODE BREAKDOWN</div>", unsafe_allow_html=True)
            if "mode" in df.columns:
                mode_counts = df["mode"].value_counts().reset_index()
                mode_counts.columns = ["Mode", "Count"]
                st.bar_chart(mode_counts.set_index("Mode")["Count"])

    # ── Top Signs Table ───────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>SIGN FREQUENCY TABLE</div>", unsafe_allow_html=True)

    if stats["top_signs"]:
        for sign, count in stats["top_signs"]:
            pct = round(count / stats["total"] * 100, 1)
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:12px; margin:4px 0">
                    <span style="font-family:var(--font-head); font-size:1.1rem; font-weight:700;
                                color:var(--cyan); min-width:60px">{sign}</span>
                    <div class="conf-bar-wrap" style="flex:1; height:6px">
                        <div class="conf-bar-fill" style="width:{pct}%"></div>
                    </div>
                    <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-secondary); min-width:80px; text-align:right">
                        {count}× ({pct}%)
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── Recent Activity ───────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>RECENT ACTIVITY</div>", unsafe_allow_html=True)
    for entry in stats.get("recent", []):
        conf_color = "#00ff88" if entry["confidence"] >= 80 else "#ffd60a" if entry["confidence"] >= 60 else "#ff2d55"
        st.markdown(
            f"""
            <div class="history-row">
                <span class="history-sign">{entry['sign']}</span>
                <span style="color:{conf_color}; font-family:var(--font-mono); font-size:0.8rem">{entry['confidence']}%</span>
                <span style="color:var(--text-muted); font-size:0.7rem">{entry.get('mode','')}</span>
                <span class="history-time">{entry['time']}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
