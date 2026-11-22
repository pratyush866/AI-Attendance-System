import streamlit as st
from src.ui.image_utils import get_image_base64

def header_home():
    logo_data = get_image_base64("logo.png")
    logo_img_tag = f"<img src='{logo_data}' style='height: 85px; width: auto; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.2)); margin-bottom: 8px;' />" if logo_data else ""

    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 15px; margin-bottom: 25px;">
            {logo_img_tag}
            <div style="display: inline-flex; align-items: center; gap: 6px; background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 9999px; padding: 4px 16px; margin-bottom: 12px; backdrop-filter: blur(8px);">
                <span style="font-size: 0.8rem; color: #fef08a; font-weight: 700; letter-spacing: 0.5px;">⚡ ORBITALS AI SYSTEM</span>
            </div>
            <h1 style="text-align: center; color: #FFFFFF; font-family: 'Outfit', sans-serif !important; font-size: 3.2rem !important; font-weight: 900 !important; letter-spacing: -1px; margin: 0; line-height: 1.1; text-shadow: 0 4px 20px rgba(0,0,0,0.25);">
                SNAP<span style="background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CLASS</span>
            </h1>
            <p style="text-align: center; color: rgba(255, 255, 255, 0.85); font-family: 'Outfit', sans-serif; font-size: 1.05rem; margin-top: 6px; max-width: 500px; font-weight: 400;">
                Smart Dual-Verification & Anti-Bunk Attendance Platform
            </p>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_data = get_image_base64("logo.png")
    logo_img_tag = f"<img src='{logo_data}' style='height: 55px; width: auto; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));' />" if logo_data else ""

    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
            {logo_img_tag}
            <div>
                <h2 style="text-align: left; color: #4338ca; font-family: 'Outfit', sans-serif !important; font-size: 1.8rem !important; font-weight: 800 !important; margin: 0; line-height: 1.1;">
                    SNAP<span style="color: #6366f1;">CLASS</span>
                </h2>
                <span style="font-size: 0.75rem; color: #64748b; font-weight: 600; letter-spacing: 0.5px; font-family: 'Outfit', sans-serif;">
                    BY ORBITALS TEAM
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)
