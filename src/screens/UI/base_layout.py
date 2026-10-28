import streamlit as st

def style_background_home():
    """Dark modern SaaS landing background with ambient glow."""
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0b0f19 75%, #07090e 100%) !important;
                color: #F8FAFC !important;
            }
            
            /* Home Card Glassmorphism */
            .home-portal-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 24px;
                padding: 2.2rem 2rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
            }
            .home-portal-card:hover {
                transform: translateY(-4px);
                border-color: rgba(99, 102, 241, 0.5);
                box-shadow: 0 25px 50px -12px rgba(79, 70, 229, 0.25);
                background: rgba(255, 255, 255, 0.08);
            }
        </style>
    """, unsafe_allow_html=True)

def style_background_dashboard():
    """Modern, clean light dashboard canvas with crisp contrast."""
    st.markdown("""
        <style>
            .stApp {
                background: #F8FAFC !important;
                color: #0F172A !important;
            }
        </style>
    """, unsafe_allow_html=True)

def style_base_layout():
    """Global modern typography, buttons, metrics, and card styling."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

        /* Clean Top Bar */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        #MainMenu, footer {
            visibility: hidden;
        }

        /* Generous widescreen layout for modern monitors */
        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 1200px !important;
            margin: 0 auto !important;
        }

        /* Modern Typography */
        html, body, .stApp, p, label, span {
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
            -webkit-font-smoothing: antialiased;
        }

        h1 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.03em !important;
            color: #0F172A !important;
            line-height: 1.2 !important;
        }

        h2 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em !important;
            color: #1E293B !important;
            line-height: 1.25 !important;
        }

        h3 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: #1E293B !important;
        }

        h4 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            color: #334155 !important;
        }

        /* Preserve Streamlit Material Symbols */
        [data-testid="stIconMaterial"], 
        .material-symbols-rounded, 
        .material-icons,
        [class*="material-symbols"] {
            font-family: 'Material Symbols Rounded' !important;
            font-weight: normal !important;
            font-style: normal !important;
            text-transform: none !important;
            letter-spacing: normal !important;
            line-height: 1 !important;
        }

        /* Modern Gradient Brand Title */
        .brand-gradient {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #2563EB 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 900 !important;
            letter-spacing: -0.04em !important;
        }

        /* Button Redesign - Sleek, Tactile, Modern */
        button {
            border-radius: 12px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.65rem 1.4rem !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid transparent !important;
        }

        /* Primary Button: Gradient Indigo Glow */
        button[kind="primary"], .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.3) !important;
            border: none !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.45) !important;
            transform: translateY(-1px) !important;
            filter: brightness(1.06) !important;
        }
        button[kind="primary"]:active {
            transform: translateY(0px) !important;
        }

        /* Secondary Button: Clean Modern Surface */
        button[kind="secondary"], .stButton > button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #334155 !important;
            border: 1.5px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        }
        button[kind="secondary"]:hover {
            background: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            color: #0F172A !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08) !important;
        }

        /* Tertiary Button: Soft Indigo Tint */
        button[kind="tertiary"], .stButton > button[kind="tertiary"] {
            background: #EEF2FF !important;
            color: #4F46E5 !important;
            border: 1px solid #C7D2FE !important;
        }
        button[kind="tertiary"]:hover {
            background: #E0E7FF !important;
            color: #3730A3 !important;
            border-color: #A5B4FC !important;
            transform: translateY(-1px) !important;
        }

        /* Elevated Metric Cards */
        div[data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 1.25rem 1.4rem !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
            transition: all 0.25s ease !important;
            position: relative;
            overflow: hidden;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.08) !important;
            border-color: #C7D2FE !important;
        }
        div[data-testid="stMetric"] label {
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            color: #64748B !important;
            margin-bottom: 0.4rem !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 1.95rem !important;
            font-weight: 800 !important;
            color: #0F172A !important;
            letter-spacing: -0.02em !important;
        }

        /* Text Input & Controls Modernization */
        div[data-baseweb="input"] {
            border-radius: 12px !important;
            border: 1.5px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #6366F1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        }
        div[data-baseweb="input"] input {
            color: #0F172A !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.95rem !important;
        }

        /* Selectboxes & Dropdowns */
        div[data-baseweb="select"] {
            border-radius: 12px !important;
        }
        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
            border: 1.5px solid #E2E8F0 !important;
            background: #FFFFFF !important;
        }

        /* Tabs Modern Styling */
        .stTabs [data-baseweb="tab-list"] {
            background: #F1F5F9 !important;
            border-radius: 14px !important;
            padding: 5px !important;
            gap: 6px !important;
            border: 1px solid #E2E8F0 !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            color: #64748B !important;
            padding: 8px 18px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
        }
        .stTabs [aria-selected="true"] {
            background: #FFFFFF !important;
            color: #4F46E5 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
        }

        /* DataTables & DataEditors */
        div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] {
            border-radius: 16px !important;
            border: 1px solid #E2E8F0 !important;
            background: #FFFFFF !important;
            box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.04) !important;
            overflow: hidden !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            color: #1E293B !important;
            padding: 12px 18px !important;
        }

        /* Dividers */
        hr {
            border-color: #E2E8F0 !important;
            opacity: 0.8 !important;
            margin: 1.5rem 0 !important;
        }

        /* Alert Banners */
        div[data-testid="stAlert"] {
            border-radius: 14px !important;
            border: none !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
        }

        /* Logout / Back button container */
        .st-key-loginbackbtn {
            display: flex;
            justify-content: flex-end;
        }
        .st-key-loginbackbtn button {
            margin-left: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)
