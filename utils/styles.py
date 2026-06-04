"""
Global CSS Styles - Dark Neon Theme
SignSpeak AI
"""

import streamlit as st


def inject_global_css():
    """Inject global CSS for the dark neon theme."""
    st.markdown(
        """
        <style>
        /* ─── Google Fonts ─── */
        @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

        /* ─── CSS Variables ─── */
        :root {
            --cyan:       #00f5ff;
            --cyan-dim:   #00b8c1;
            --blue:       #0080ff;
            --blue-dim:   #0055aa;
            --green:      #00ff88;
            --green-dim:  #00aa55;
            --purple:     #bf00ff;
            --red:        #ff2d55;
            --yellow:     #ffd60a;
            --bg-primary:   #050a14;
            --bg-secondary: #0a1628;
            --bg-card:      #0d1f38;
            --bg-card-hover:#112440;
            --border:       rgba(0,245,255,0.18);
            --border-bright:rgba(0,245,255,0.5);
            --text-primary: #e8f4fd;
            --text-secondary:#8ab0cc;
            --text-muted:   #4a6580;
            --font-main:    'Exo 2', sans-serif;
            --font-mono:    'Share Tech Mono', monospace;
            --font-head:    'Rajdhani', sans-serif;
            --glow-cyan: 0 0 10px rgba(0,245,255,0.5), 0 0 20px rgba(0,245,255,0.25), 0 0 40px rgba(0,245,255,0.1);
            --glow-blue: 0 0 10px rgba(0,128,255,0.5), 0 0 20px rgba(0,128,255,0.25);
            --glow-green:0 0 10px rgba(0,255,136,0.5), 0 0 20px rgba(0,255,136,0.25);
        }

        /* ─── App Background ─── */
        .stApp {
            background: var(--bg-primary);
            background-image:
                radial-gradient(ellipse at 20% 20%, rgba(0,80,160,0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(0,100,80,0.1) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(0,30,60,0.3) 0%, transparent 100%);
            font-family: var(--font-main);
            color: var(--text-primary);
        }

        /* ─── Hide Streamlit Defaults ─── */
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

        /* ─── Scrollbar ─── */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--cyan-dim); border-radius: 3px; }

        /* ─── Sidebar ─── */
        [data-testid="stSidebar"] {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border) !important;
        }
        [data-testid="stSidebar"] > div { padding: 0 !important; }

        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 20px 16px 16px 16px;
        }
        .logo-icon {
            font-size: 2.2rem;
            filter: drop-shadow(0 0 8px rgba(0,245,255,0.6));
        }
        .logo-text { display: flex; flex-direction: column; }
        .logo-main {
            font-family: var(--font-head);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--cyan);
            text-shadow: var(--glow-cyan);
            letter-spacing: 2px;
            line-height: 1;
        }
        .logo-sub {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .sidebar-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-bright), transparent);
            margin: 8px 0;
        }

        .nav-label {
            font-family: var(--font-mono);
            font-size: 0.6rem;
            color: var(--text-muted);
            letter-spacing: 3px;
            padding: 8px 16px 4px 16px;
            margin: 0;
        }

        /* Nav buttons */
        [data-testid="stSidebar"] .stButton button {
            background: transparent !important;
            border: none !important;
            color: var(--text-secondary) !important;
            font-family: var(--font-main) !important;
            font-size: 0.85rem !important;
            font-weight: 400 !important;
            text-align: left !important;
            padding: 8px 16px !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
            letter-spacing: 0.5px;
        }
        [data-testid="stSidebar"] .stButton button:hover {
            background: rgba(0,245,255,0.08) !important;
            color: var(--cyan) !important;
            transform: translateX(4px) !important;
        }

        .sidebar-stats {
            display: flex;
            gap: 8px;
            padding: 12px 16px;
        }
        .stat-item {
            flex: 1;
            background: rgba(0,245,255,0.05);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 8px;
            text-align: center;
        }
        .stat-val {
            display: block;
            font-family: var(--font-head);
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--cyan);
        }
        .stat-lbl {
            font-family: var(--font-mono);
            font-size: 0.6rem;
            color: var(--text-muted);
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        .sidebar-footer {
            padding: 12px 16px;
            text-align: center;
        }
        .sidebar-footer p {
            font-family: var(--font-mono);
            font-size: 0.6rem;
            color: var(--text-muted);
            margin: 2px 0;
        }

        /* ─── Page Headers ─── */
        .page-header {
            text-align: center;
            padding: 2rem 0 1.5rem 0;
            position: relative;
        }
        .page-header::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 10%;
            right: 10%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-bright), transparent);
        }
        .page-title {
            font-family: var(--font-head);
            font-size: 2.8rem;
            font-weight: 700;
            letter-spacing: 4px;
            text-transform: uppercase;
            background: linear-gradient(135deg, var(--cyan), var(--blue), var(--green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            display: inline-block;
        }
        .page-subtitle {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* ─── Cards ─── */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--cyan), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .card:hover { border-color: var(--border-bright); transform: translateY(-2px); }
        .card:hover::before { opacity: 1; }

        .card-cyan  { border-color: rgba(0,245,255,0.3); }
        .card-blue  { border-color: rgba(0,128,255,0.3); }
        .card-green { border-color: rgba(0,255,136,0.3); }
        .card-red   { border-color: rgba(255,45,85,0.3); }

        /* ─── Prediction Display ─── */
        .prediction-box {
            background: linear-gradient(135deg, rgba(0,245,255,0.05), rgba(0,128,255,0.05));
            border: 2px solid var(--cyan);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            box-shadow: var(--glow-cyan);
            animation: pulse-border 2s ease-in-out infinite;
        }
        @keyframes pulse-border {
            0%, 100% { box-shadow: 0 0 10px rgba(0,245,255,0.3); }
            50%       { box-shadow: 0 0 25px rgba(0,245,255,0.6), 0 0 50px rgba(0,245,255,0.2); }
        }
        .prediction-letter {
            font-family: var(--font-head);
            font-size: 5rem;
            font-weight: 900;
            color: var(--cyan);
            text-shadow: var(--glow-cyan);
            line-height: 1;
        }
        .prediction-word {
            font-family: var(--font-head);
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--green);
            text-shadow: var(--glow-green);
        }
        .confidence-label {
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--text-muted);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 8px;
        }

        /* ─── Confidence Bar ─── */
        .conf-bar-wrap {
            background: rgba(255,255,255,0.05);
            border-radius: 50px;
            overflow: hidden;
            height: 8px;
            margin: 8px 0;
        }
        .conf-bar-fill {
            height: 100%;
            border-radius: 50px;
            background: linear-gradient(90deg, var(--blue), var(--cyan));
            box-shadow: 0 0 8px rgba(0,245,255,0.5);
            transition: width 0.4s ease;
        }

        /* ─── Word Display ─── */
        .word-display {
            background: rgba(0,255,136,0.05);
            border: 1px solid rgba(0,255,136,0.3);
            border-radius: 10px;
            padding: 1rem 1.5rem;
            font-family: var(--font-head);
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--green);
            letter-spacing: 6px;
            text-align: center;
            margin: 8px 0;
        }
        .sentence-display {
            background: rgba(0,128,255,0.05);
            border: 1px solid rgba(0,128,255,0.3);
            border-radius: 10px;
            padding: 1rem 1.5rem;
            font-family: var(--font-main);
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
            text-align: center;
            margin: 8px 0;
        }

        /* ─── Letter Chips ─── */
        .letter-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            padding: 12px 0;
        }
        .letter-chip {
            background: rgba(0,245,255,0.1);
            border: 1px solid rgba(0,245,255,0.4);
            border-radius: 8px;
            padding: 8px 14px;
            font-family: var(--font-head);
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--cyan);
            animation: chip-appear 0.3s ease;
        }
        @keyframes chip-appear {
            from { transform: scale(0.5); opacity: 0; }
            to   { transform: scale(1);   opacity: 1; }
        }

        /* ─── Status Badges ─── */
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 12px;
            border-radius: 50px;
            font-family: var(--font-mono);
            font-size: 0.7rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }
        .badge-green { background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.4); color: var(--green); }
        .badge-cyan  { background: rgba(0,245,255,0.1); border: 1px solid rgba(0,245,255,0.4); color: var(--cyan); }
        .badge-red   { background: rgba(255,45,85,0.1);  border: 1px solid rgba(255,45,85,0.4);  color: var(--red); }
        .badge-dot   { width: 6px; height: 6px; border-radius: 50%; background: currentColor; animation: blink 1.2s ease infinite; }
        @keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.2; } }

        /* ─── Metric Cards ─── */
        .metric-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .metric-card::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
        }
        .metric-card-cyan::after  { background: linear-gradient(90deg, transparent, var(--cyan), transparent); }
        .metric-card-green::after { background: linear-gradient(90deg, transparent, var(--green), transparent); }
        .metric-card-blue::after  { background: linear-gradient(90deg, transparent, var(--blue), transparent); }
        .metric-val {
            font-family: var(--font-head);
            font-size: 2.5rem;
            font-weight: 700;
        }
        .metric-lbl {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-top: 4px;
        }

        /* ─── Emergency Buttons ─── */
        .emergency-btn {
            background: linear-gradient(135deg, rgba(255,45,85,0.15), rgba(255,45,85,0.05));
            border: 2px solid rgba(255,45,85,0.6) !important;
            border-radius: 16px !important;
            color: #ff6680 !important;
            font-family: var(--font-head) !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            letter-spacing: 2px !important;
            padding: 20px !important;
            transition: all 0.2s ease !important;
            text-transform: uppercase !important;
        }
        .emergency-btn:hover {
            background: linear-gradient(135deg, rgba(255,45,85,0.3), rgba(255,45,85,0.15)) !important;
            box-shadow: 0 0 20px rgba(255,45,85,0.4) !important;
            transform: scale(1.02) !important;
        }

        /* ─── Learning Cards ─── */
        .sign-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .sign-card:hover {
            border-color: var(--cyan);
            box-shadow: 0 0 15px rgba(0,245,255,0.2);
            transform: translateY(-4px);
        }
        .sign-letter {
            font-family: var(--font-head);
            font-size: 2.5rem;
            font-weight: 900;
            color: var(--cyan);
        }
        .sign-emoji {
            font-size: 2rem;
            display: block;
            margin: 8px 0;
        }
        .sign-desc {
            font-family: var(--font-mono);
            font-size: 0.65rem;
            color: var(--text-muted);
            letter-spacing: 1px;
        }

        /* ─── Streamlit Component Overrides ─── */
        .stButton button {
            background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(0,128,255,0.1)) !important;
            border: 1px solid var(--border-bright) !important;
            color: var(--cyan) !important;
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
            letter-spacing: 1px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        .stButton button:hover {
            background: linear-gradient(135deg, rgba(0,245,255,0.2), rgba(0,128,255,0.2)) !important;
            box-shadow: var(--glow-cyan) !important;
            transform: translateY(-1px) !important;
        }
        .stButton button:active { transform: translateY(0) !important; }

        /* Selectbox, text input */
        .stSelectbox select,
        .stTextInput input,
        .stTextArea textarea {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-main) !important;
            border-radius: 8px !important;
        }
        .stSelectbox select:focus,
        .stTextInput input:focus {
            border-color: var(--cyan) !important;
            box-shadow: 0 0 0 2px rgba(0,245,255,0.1) !important;
        }

        /* Slider */
        .stSlider [data-baseweb="slider"] { color: var(--cyan) !important; }

        /* Progress bar */
        .stProgress > div > div { background: linear-gradient(90deg, var(--blue), var(--cyan)) !important; }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--bg-card) !important;
            border-radius: 10px !important;
            border: 1px solid var(--border) !important;
            padding: 4px !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: var(--text-muted) !important;
            font-family: var(--font-main) !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(0,245,255,0.1) !important;
            color: var(--cyan) !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-main) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
        }

        /* Dataframe */
        .stDataFrame { border: 1px solid var(--border) !important; border-radius: 8px !important; }

        /* Metric */
        [data-testid="stMetric"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }
        [data-testid="stMetricValue"] {
            color: var(--cyan) !important;
            font-family: var(--font-head) !important;
            font-weight: 700 !important;
        }

        /* File uploader */
        [data-testid="stFileUploader"] {
            border: 2px dashed var(--border-bright) !important;
            border-radius: 12px !important;
            background: rgba(0,245,255,0.02) !important;
        }

        /* Camera input */
        [data-testid="stCameraInput"] { border-radius: 12px !important; overflow: hidden; }

        /* ─── Animations ─── */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes scanline {
            0%   { transform: translateY(-100%); }
            100% { transform: translateY(100vh); }
        }
        .fade-in-up { animation: fadeInUp 0.6s ease forwards; }

        /* ─── Home Hero ─── */
        .hero-section {
            text-align: center;
            padding: 3rem 1rem;
            position: relative;
        }
        .hero-title {
            font-family: var(--font-head);
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: 8px;
            text-transform: uppercase;
            background: linear-gradient(135deg, var(--cyan), var(--blue) 50%, var(--green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            margin-bottom: 8px;
        }
        .hero-tagline {
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--text-muted);
            letter-spacing: 5px;
            text-transform: uppercase;
            margin-bottom: 2rem;
        }

        /* ─── Toast/Notification ─── */
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--bg-card);
            border: 1px solid var(--cyan);
            border-radius: 10px;
            padding: 12px 20px;
            color: var(--cyan);
            font-family: var(--font-mono);
            font-size: 0.8rem;
            z-index: 9999;
            animation: fadeInUp 0.4s ease;
            box-shadow: var(--glow-cyan);
        }

        /* ─── Section Headers ─── */
        .section-header {
            font-family: var(--font-head);
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--cyan);
            letter-spacing: 3px;
            text-transform: uppercase;
            margin: 1.5rem 0 0.8rem 0;
            padding-bottom: 6px;
            border-bottom: 1px solid var(--border);
        }

        /* ─── Accessibility Mode ─── */
        .a11y-large .prediction-letter { font-size: 8rem !important; }
        .a11y-large .page-title { font-size: 3.5rem !important; }
        .a11y-large .stButton button { font-size: 1.2rem !important; padding: 16px 24px !important; }
        .a11y-contrast { filter: contrast(1.5) brightness(1.1); }

        /* History table row */
        .history-row {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 8px;
            margin: 4px 0;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            color: var(--text-secondary);
            transition: background 0.2s;
        }
        .history-row:hover { background: var(--bg-card-hover); }
        .history-sign { color: var(--cyan); font-weight: 700; min-width: 80px; font-size: 1rem; }
        .history-conf { color: var(--green); min-width: 60px; }
        .history-time { color: var(--text-muted); flex: 1; text-align: right; }
        </style>
        """,
        unsafe_allow_html=True,
    )
