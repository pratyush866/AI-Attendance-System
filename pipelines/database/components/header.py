import streamlit as st
from pipelines.database.config import is_db_connected

def header_home():
    logo_url = "assets/snapclass_logo.jpg"
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:10px;">
            <div style="position:relative; display:inline-block;">
                <div style="position:absolute; inset:-4px; background:linear-gradient(135deg, #4F46E5, #818CF8); border-radius:24px; filter:blur(10px); opacity:0.6;"></div>
                <img src='{logo_url}' style='height:88px; width:88px; object-fit:contain; position:relative; background:#0F172A; border-radius:22px; padding:10px; border:1px solid rgba(255,255,255,0.15);' />
            </div>
            <h1 style='text-align:center; font-family:"Plus Jakarta Sans", sans-serif; font-size:3.2rem; font-weight:900; margin:16px 0 6px 0; letter-spacing:-0.04em; background:linear-gradient(135deg, #FFFFFF 0%, #E0E7FF 60%, #A5B4FC 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
                SNAPCLASS
            </h1>
            <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
                <span style="background:rgba(99, 102, 241, 0.15); color:#A5B4FC; border:1px solid rgba(165, 180, 252, 0.3); padding:4px 14px; border-radius:999px; font-size:0.82rem; font-weight:600; letter-spacing:0.02em;">
                    ⚡ AI Biometric Attendance System
                </span>
            </div>
        </div>   
    """, unsafe_allow_html=True)

def header_dashboard():
    logo_url = "assets/snapclass_logo.jpg"
    connected = is_db_connected()
    badge_html = (
        "<span style='background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; padding:4px 12px; border-radius:999px; font-size:0.75rem; font-weight:700; display:inline-flex; align-items:center; gap:5px; box-shadow:0 1px 2px rgba(0,0,0,0.03);'><span style='height:6px; width:6px; border-radius:50%; background:#10B981;'></span> Cloud Supabase Synced</span>"
        if connected
        else "<span style='background:#FFFBEB; color:#B45309; border:1px solid #FDE68A; padding:4px 12px; border-radius:999px; font-size:0.75rem; font-weight:700; display:inline-flex; align-items:center; gap:5px;'><span style='height:6px; width:6px; border-radius:50%; background:#F59E0B;'></span> Local SQLite Active</span>"
    )
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:flex-start; gap:14px; flex-wrap:wrap; padding-bottom:6px;">
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:18px; padding:6px; box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                <img src='{logo_url}' style='height:52px; width:52px; object-fit:contain;' />
            </div>
            <div>
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style='font-family:"Plus Jakarta Sans", sans-serif; font-size:1.65rem; font-weight:900; letter-spacing:-0.03em; background:linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
                        SNAPCLASS
                    </span>
                    {badge_html}
                </div>
                <div style="color:#64748B; font-size:0.82rem; font-weight:500; margin-top:1px;">
                    Automated Face & Voice Attendance Platform
                </div>
            </div>
        </div>   
    """, unsafe_allow_html=True)
