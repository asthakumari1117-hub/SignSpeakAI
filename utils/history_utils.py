"""
History & Statistics Utilities
SignSpeak AI
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime


HISTORY_FILE = "history/predictions.json"
os.makedirs("history", exist_ok=True)


# ─── Record prediction ─────────────────────────────────────────────────────────
def record_prediction(sign: str, confidence: float, mode: str = "live"):
    """Save a prediction to session state and persistent history."""
    entry = {
        "time":       datetime.now().strftime("%H:%M:%S"),
        "date":       datetime.now().strftime("%Y-%m-%d"),
        "sign":       sign,
        "confidence": round(confidence, 2),
        "mode":       mode,
    }

    # Session state
    st.session_state.prediction_history.insert(0, entry)
    st.session_state.prediction_history = st.session_state.prediction_history[:200]
    st.session_state.total_predictions += 1

    # Sign counts
    counts = st.session_state.get("sign_counts", {})
    counts[sign] = counts.get(sign, 0) + 1
    st.session_state.sign_counts = counts

    # Persist to file
    _append_history(entry)


def _append_history(entry: dict):
    """Append to local JSON history file."""
    try:
        records = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                records = json.load(f)
        records.insert(0, entry)
        records = records[:500]
        with open(HISTORY_FILE, "w") as f:
            json.dump(records, f, indent=2)
    except Exception:
        pass


def load_history_df() -> pd.DataFrame:
    """Load history into a DataFrame."""
    records = st.session_state.get("prediction_history", [])
    if not records:
        return pd.DataFrame(columns=["time", "date", "sign", "confidence", "mode"])
    return pd.DataFrame(records)


def export_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def export_txt(df: pd.DataFrame) -> bytes:
    lines = ["SignSpeak AI - Prediction History", "=" * 40]
    for _, row in df.iterrows():
        lines.append(f"[{row['date']} {row['time']}] {row['sign']} ({row['confidence']}%)")
    return "\n".join(lines).encode("utf-8")


# ─── Statistics ───────────────────────────────────────────────────────────────
def get_stats() -> dict:
    """Compute statistics from session history."""
    history = st.session_state.get("prediction_history", [])
    counts  = st.session_state.get("sign_counts", {})
    total   = st.session_state.get("total_predictions", 0)

    if not history:
        return {
            "total": 0,
            "avg_conf": 0.0,
            "top_signs": [],
            "recent": [],
        }

    df = pd.DataFrame(history)
    avg_conf = round(df["confidence"].mean(), 1)

    top_signs = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "total":     total,
        "avg_conf":  avg_conf,
        "top_signs": top_signs,
        "recent":    history[:10],
        "df":        df,
    }
