import streamlit as st

def footer_home():
    st.markdown(
        """
        <div style="margin-top:3.5rem; text-align:center; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.08);">
            <div style="color:rgba(255,255,255,0.7); font-size:0.85rem; font-weight:500;">
                SnapClass AI Attendance System &bull; Crafted with precision &bull; Fast, Accurate & Scalable
            </div>
            <div style="color:rgba(255,255,255,0.4); font-size:0.75rem; margin-top:4px;">
                ResNet-34 128D Face Embeddings &bull; Resemblyzer Voice Biometrics &bull; College Reports
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def footer_dashboard():
    st.markdown(
        """
        <div style="margin-top:3.5rem; text-align:center; padding-top:1.5rem; border-top:1px solid #E2E8F0;">
            <div style="color:#64748B; font-size:0.85rem; font-weight:500;">
                SnapClass AI Attendance Portal &bull; Academic Year 2026-2027
            </div>
            <div style="color:#94A3B8; font-size:0.75rem; margin-top:4px;">
                Multi-photo Face Analysis &bull; Manual Overrides &bull; Roll No Wise Consolidated Registers
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
