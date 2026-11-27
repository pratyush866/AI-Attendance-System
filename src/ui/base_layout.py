import streamlit as st

def style_background_home():
    st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 12% 18%, rgba(167, 139, 250, 0.28) 0%, transparent 42%),
        radial-gradient(circle at 88% 15%, rgba(129, 140, 248, 0.30) 0%, transparent 45%),
        radial-gradient(circle at 75% 82%, rgba(244, 114, 182, 0.16) 0%, transparent 45%),
        linear-gradient(135deg, #f5f3ff 0%, #ede9fe 48%, #e8eafd 100%) !important;
    min-height: 100vh;
    color: #0f172a !important;
}

.block-container {
    max-width: 1180px !important;
    margin: 0 auto !important;
    padding-top: 1.1rem !important;
    padding-bottom: 1.8rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* Floating White Glass Navbar Pill */
.st-key-navbar_pill {
    background: rgba(255, 255, 255, 0.90) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(199, 210, 254, 0.75) !important;
    border-radius: 9999px !important;
    padding: 0.45rem 1.25rem !important;
    box-shadow: 0 10px 30px -8px rgba(79, 70, 229, 0.12) !important;
    margin-bottom: 1.4rem !important;
}

.st-key-navbar_pill button[data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 6px 12px !important;
    border-radius: 9999px !important;
    white-space: nowrap !important;
}

.st-key-navbar_pill button[data-testid="stBaseButton-secondary"]:hover {
    background: #eef2ff !important;
    color: #4f46e5 !important;
    transform: none !important;
}

.st-key-navbar_pill button[data-testid="stBaseButton-primary"] {
    background: #eef2ff !important;
    color: #4338ca !important;
    border: 1px solid #c7d2fe !important;
    box-shadow: none !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 6px 14px !important;
    border-radius: 9999px !important;
    white-space: nowrap !important;
}

/* Student Role Card */
.st-key-student_card {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1.5px solid rgba(129, 140, 248, 0.35) !important;
    border-radius: 26px !important;
    padding: 1.6rem 1.6rem 1.4rem 1.6rem !important;
    box-shadow: 0 20px 45px -15px rgba(79, 70, 229, 0.16), 0 4px 12px rgba(15, 23, 42, 0.03) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

.st-key-student_card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 28px 55px -15px rgba(79, 70, 229, 0.24) !important;
}

.st-key-student_card button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(90deg, #4338ca 0%, #6366f1 55%, #7c3aed 100%) !important;
    border-radius: 9999px !important;
    padding: 0.72rem 1.5rem !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    box-shadow: 0 10px 22px -6px rgba(79, 70, 229, 0.45) !important;
}

/* Teacher Role Card */
.st-key-teacher_card {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1.5px solid rgba(244, 114, 182, 0.35) !important;
    border-radius: 26px !important;
    padding: 1.6rem 1.6rem 1.4rem 1.6rem !important;
    box-shadow: 0 20px 45px -15px rgba(219, 39, 119, 0.14), 0 4px 12px rgba(15, 23, 42, 0.03) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
}

.st-key-teacher_card:hover {
    transform: translateY(-4px) !important;
    box-shadow: 0 28px 55px -15px rgba(219, 39, 119, 0.22) !important;
}

.st-key-teacher_card button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(90deg, #db2777 0%, #ec4899 55%, #f43f5e 100%) !important;
    border-radius: 9999px !important;
    padding: 0.72rem 1.5rem !important;
    font-size: 0.98rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    box-shadow: 0 10px 22px -6px rgba(219, 39, 119, 0.42) !important;
}

@media (max-width: 768px) {
    .st-key-navbar_pill {
        border-radius: 20px !important;
        padding: 0.75rem 1rem !important;
    }
    .st-key-student_card, .st-key-teacher_card {
        padding: 1.25rem !important;
        border-radius: 20px !important;
    }
}
</style>
""", unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
<style>
.stApp {
    background: #f8fafc !important;
    color: #0f172a !important;
}

.block-container {
    max-width: 980px !important;
    margin: 0 auto !important;
}

/* Fix contrast: Force all headers and texts to deep, crisp charcoal colors on dashboard */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    color: #0f172a !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
}

.stApp p, .stApp label, .stApp span:not([data-testid="stIconMaterial"]) {
    color: #334155 !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Keep Streamlit card containers clean */
.stApp div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}
</style>
""", unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* Hide Streamlit top bar decorations */
#MainMenu, footer, header {
    visibility: hidden;
    display: none !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 980px !important;
    margin: 0 auto !important;
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif !important;
    color: #0f172a !important;
}

p, label, span:not([data-testid="stIconMaterial"]) {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Restore material icons font */
span[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    font-style: normal !important;
    font-weight: normal !important;
    display: inline-block !important;
    line-height: 1 !important;
}

/* Primary Action Buttons */
button[data-testid="stBaseButton-primary"], button[kind="primary"] {
    border-radius: 14px !important;
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    padding: 10px 22px !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

button[data-testid="stBaseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.45) !important;
}

/* Secondary Action Buttons */
button[data-testid="stBaseButton-secondary"], button[kind="secondary"] {
    border-radius: 14px !important;
    background: #ffffff !important;
    color: #1e293b !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    transition: all 0.2s ease !important;
}

button[data-testid="stBaseButton-secondary"]:hover {
    background: #f8fafc !important;
    border-color: #94a3b8 !important;
    transform: translateY(-2px) !important;
}

/* Tertiary / Danger Unenroll Buttons */
.tertiary-btn button, .tertiary-btn div[data-testid="stButton"] button {
    border-radius: 12px !important;
    background: #fef2f2 !important;
    color: #dc2626 !important;
    font-weight: 600 !important;
    padding: 8px 16px !important;
    border: 1px solid #fecaca !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

.tertiary-btn button:hover {
    background: #fee2e2 !important;
    color: #b91c1c !important;
    border-color: #f87171 !important;
    transform: translateY(-2px) !important;
}

/* =======================================================
   RESPONSIVE MOBILE VIEW (Phone / Small Tablets)
   ======================================================= */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        padding-top: 1rem !important;
    }

    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 12px !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        width: 100% !important;
        min-width: 100% !important;
        flex: 1 1 100% !important;
        margin-bottom: 8px !important;
    }

    h1 {
        font-size: 2.1rem !important;
        line-height: 1.15 !important;
    }

    h2 {
        font-size: 1.55rem !important;
        line-height: 1.2 !important;
    }

    h3 {
        font-size: 1.25rem !important;
    }

    button {
        width: 100% !important;
        padding: 12px 18px !important;
    }
}
</style>
""", unsafe_allow_html=True)
