import streamlit as st

def footer_home():
    st.markdown("""
<div style="margin-top:2rem;padding-top:1.1rem;border-top:1px solid rgba(148,163,184,0.22);display:flex;flex-direction:column;align-items:center;gap:10px;">
<div style="display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:28px;font-family:'Plus Jakarta Sans',sans-serif;font-size:0.9rem;font-weight:600;color:#334155;">
<span style="display:inline-flex;align-items:center;gap:7px;">
<span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:rgba(79,70,229,0.12);color:#4f46e5;">🛡️</span>
Trusted &amp; Secure
</span>
<span style="color:#cbd5e1;">|</span>
<span style="display:inline-flex;align-items:center;gap:7px;">
<span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:rgba(245,158,11,0.15);color:#d97706;">⚡</span>
Fast &amp; Reliable
</span>
<span style="color:#cbd5e1;">|</span>
<span style="display:inline-flex;align-items:center;gap:7px;">
<span style="display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:rgba(236,72,153,0.14);color:#db2777;">💗</span>
Built for a Smarter Campus
</span>
</div>
<div style="color:#64748b;font-size:0.78rem;font-family:'Outfit',sans-serif;text-align:center;">
Developed by <strong style="color:#4338ca;">Orbitals Team</strong> • ITM College of Science &amp; Management, Gorakhpur
</div>
</div>
""", unsafe_allow_html=True)


def footer_dashboard():
    st.markdown("""
<div style="margin-top:3rem;margin-bottom:1rem;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;">
<div style="display:inline-flex;align-items:center;gap:8px;background:white;padding:6px 18px;border-radius:9999px;border:1px solid #e2e8f0;box-shadow:0 2px 10px rgba(0,0,0,0.04);">
<span style="color:#64748b;font-size:0.9rem;font-weight:500;font-family:'Outfit',sans-serif;">
Created with ❤️ by
</span>
<span style="background:linear-gradient(135deg,#4f46e5,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:800;font-size:1.05rem;letter-spacing:0.5px;font-family:'Outfit',sans-serif;">
✦ Orbitals team
</span>
</div>
</div>
""", unsafe_allow_html=True)
