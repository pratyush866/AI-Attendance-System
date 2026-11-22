import streamlit as st

def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background: radial-gradient(135% 125% at 50% 5%, #4f46e5 0%, #3730a3 45%, #1e1b4b 100%) !important;
                min-height: 100vh;
            }

            .stApp div[data-testid="stColumn"] {
                background: #ffffff !important;
                padding: 2.2rem 2rem !important;
                border-radius: 28px !important;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.15) !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                transform: translateY(-5px) !important;
                box-shadow: 0 35px 60px -15px rgba(0, 0, 0, 0.45) !important;
            }

            /* Responsive on Phone View */
            @media (max-width: 768px) {
                .stApp div[data-testid="stColumn"] {
                    padding: 1.5rem 1.2rem !important;
                    margin-bottom: 1.2rem !important;
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
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

            /* Hide Streamlit top bar decorations */
            #MainMenu, footer, header {
                visibility: hidden;
                display: none !important;
            }
                
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                max-width: 960px !important;
            }

            /* Crucial: DO NOT override font-family on material icons, prevents icon text from overwriting button labels! */
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

                /* Collapse multi-column layouts into beautiful mobile stacked cards */
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
                    font-size: 2.2rem !important;
                    line-height: 1.15 !important;
                }

                h2 {
                    font-size: 1.6rem !important;
                    line-height: 1.2 !important;
                }

                h3 {
                    font-size: 1.25rem !important;
                }

                /* Mobile button sizing */
                button {
                    width: 100% !important;
                    padding: 12px 18px !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)
