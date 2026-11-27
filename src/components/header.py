import streamlit as st

GRAD_CAP_SVG = """
<svg width="34" height="34" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="capGrad" x1="0" y1="0" x2="36" y2="36" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#4338ca"/>
<stop offset="100%" stop-color="#7c3aed"/>
</linearGradient>
</defs>
<rect width="36" height="36" rx="10" fill="url(#capGrad)" fill-opacity="0.12"/>
<path d="M18 8L5 14.5L18 21L31 14.5L18 8Z" fill="url(#capGrad)"/>
<path d="M9.5 18.2V24.5C9.5 26.2 13.3 28 18 28C22.7 28 26.5 26.2 26.5 24.5V18.2L18 22.5L9.5 18.2Z" fill="#6366f1"/>
<path d="M29.5 15.2V23.5" stroke="#4f46e5" stroke-width="2" stroke-linecap="round"/>
<circle cx="29.5" cy="24.5" r="1.5" fill="#7c3aed"/>
</svg>
"""


def header_home():
    """Kept for backward compatibility; home_screen renders the unified SaaS navbar."""
    pass


def header_dashboard():
    st.markdown(f"""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
{GRAD_CAP_SVG}
<div>
<h2 style="text-align:left;color:#0f172a;font-family:'Outfit',sans-serif !important;font-size:1.7rem !important;font-weight:900 !important;margin:0;line-height:1.1;letter-spacing:-0.4px;">
SNAP<span style="background:linear-gradient(135deg,#4338ca,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CLASS</span>
</h2>
<span style="font-size:0.74rem;color:#64748b;font-weight:600;letter-spacing:0.6px;font-family:'Outfit',sans-serif;">
BY ORBITALS TEAM • AI ATTENDANCE
</span>
</div>
</div>
""", unsafe_allow_html=True)
