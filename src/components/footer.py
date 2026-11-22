import streamlit as st

def footer_home():
    st.markdown("""
        <div style="margin-top: 3.5rem; margin-bottom: 1.5rem; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); padding: 8px 22px; border-radius: 9999px; border: 1px solid rgba(255, 255, 255, 0.25); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);">
                <span style="color: rgba(255, 255, 255, 0.9); font-size: 0.95rem; font-weight: 500; font-family: 'Outfit', sans-serif;">
                    Created with ❤️ by
                </span>
                <span style="background: linear-gradient(135deg, #FFD166 0%, #FF6B6B 50%, #FF758C 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.5px; font-family: 'Outfit', sans-serif;">
                    ✦ Orbitals team
                </span>
            </div>
            <div style="color: rgba(255, 255, 255, 0.6); font-size: 0.8rem; font-family: 'Outfit', sans-serif;">
                Next-Gen AI Attendance & Dual-Verification Platform
            </div>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
    st.markdown("""
        <div style="margin-top: 3rem; margin-bottom: 1rem; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: white; padding: 6px 18px; border-radius: 9999px; border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);">
                <span style="color: #64748b; font-size: 0.9rem; font-weight: 500; font-family: 'Outfit', sans-serif;">
                    Created with ❤️ by
                </span>
                <span style="background: linear-gradient(135deg, #4f46e5, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; font-size: 1.05rem; letter-spacing: 0.5px; font-family: 'Outfit', sans-serif;">
                    ✦ Orbitals team
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)
