import streamlit as st
from pipelines.database.components.header import header_home
from pipelines.database.components.footer import footer_home
from src.screens.UI.base_layout import style_base_layout, style_background_home

def home_screen():
    style_background_home()
    style_base_layout()
    header_home()

    # Subtitle / Hero Intro
    st.markdown(
        """
        <div style="text-align:center; max-width:680px; margin:0 auto 2.5rem auto;">
            <p style="color:#94A3B8; font-size:1.1rem; line-height:1.6; margin:0;">
                Next-generation automated attendance platform powered by computer vision and voice biometrics. 
                Experience instant classroom verification, live teacher overrides, and official college reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Portal Cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div style="background:rgba(255, 255, 255, 0.04); border:1px solid rgba(255, 255, 255, 0.1); border-radius:24px; padding:2rem 1.8rem; height:100%; display:flex; flex-direction:column; backdrop-filter:blur(16px); box-shadow:0 20px 40px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                    <span style="font-size:2.4rem;">🎓</span>
                    <span style="background:rgba(99, 102, 241, 0.15); color:#A5B4FC; border:1px solid rgba(165, 180, 252, 0.25); padding:3px 12px; border-radius:999px; font-size:0.75rem; font-weight:700;">STUDENT</span>
                </div>
                <h3 style="color:#FFFFFF; font-size:1.55rem; font-weight:800; margin:0 0 8px 0; letter-spacing:-0.02em;">Student Portal</h3>
                <img src="assets/student_mascot.jpg" style="width:100%; max-height:200px; object-fit:contain; border-radius:12px; margin-bottom:8px;" />
                <p style="color:#94A3B8; font-size:0.92rem; line-height:1.5; margin-bottom:1.4rem;">
                    Authenticate in seconds using Face ID or Voice recognition, enroll in subjects, and track attendance.
                </p>
                <div style="color:#CBD5E1; font-size:0.88rem; display:flex; flex-direction:column; gap:8px; margin-bottom:1.8rem;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981;">✔</span> 1-Tap Biometric Face & Voice Login
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981;">✔</span> Self-Enrollment with Subject Codes / QR
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981;">✔</span> Real-Time Attendance & Shortage Alerts (<75%)
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)
        if st.button('Enter Student Portal →', type='primary', key="btn_student_portal", use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown(
            """
            <div style="background:rgba(255, 255, 255, 0.04); border:1px solid rgba(255, 255, 255, 0.1); border-radius:24px; padding:2rem 1.8rem; height:100%; display:flex; flex-direction:column; backdrop-filter:blur(16px); box-shadow:0 20px 40px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                    <span style="font-size:2.4rem;">👨‍🏫</span>
                    <span style="background:rgba(244, 63, 94, 0.15); color:#FDA4AF; border:1px solid rgba(253, 164, 175, 0.25); padding:3px 12px; border-radius:999px; font-size:0.75rem; font-weight:700;">FACULTY</span>
                </div>
                <h3 style="color:#FFFFFF; font-size:1.55rem; font-weight:800; margin:0 0 8px 0; letter-spacing:-0.02em;">Faculty Portal</h3>
                <img src="assets/teacher_mascot.jpg" style="width:100%; max-height:200px; object-fit:contain; border-radius:12px; margin-bottom:8px;" />
                <p style="color:#94A3B8; font-size:0.92rem; line-height:1.5; margin-bottom:1.4rem;">
                    Manage courses, scan classroom photos, tune AI sensitivity, toggle overrides, and export college registers.
                </p>
                <div style="color:#CBD5E1; font-size:0.88rem; display:flex; flex-direction:column; gap:8px; margin-bottom:1.8rem;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981;">✔</span> Multi-Photo Face Recognition & Voice Scan
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981;">✔</span> Manual Checkbox Override (Present ✅ / Absent ❌)
                    </div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981;">✔</span> Roll No-wise Monthly College Excel Reports
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top: -10px;'></div>", unsafe_allow_html=True)
        if st.button('Enter Faculty Portal →', type='primary', key="btn_teacher_portal", use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # Features Pill Bar
    st.markdown(
        """
        <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-top:3rem;">
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); padding:8px 18px; border-radius:999px; color:#E2E8F0; font-size:0.82rem; font-weight:600; display:flex; align-items:center; gap:6px;">
                <span>🎯</span> Nearest-Neighbor Matching
            </div>
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); padding:8px 18px; border-radius:999px; color:#E2E8F0; font-size:0.82rem; font-weight:600; display:flex; align-items:center; gap:6px;">
                <span>⚡</span> Sub-second Multi-face Processing
            </div>
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); padding:8px 18px; border-radius:999px; color:#E2E8F0; font-size:0.82rem; font-weight:600; display:flex; align-items:center; gap:6px;">
                <span>📊</span> University Excel Registers (.xlsx)
            </div>
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); padding:8px 18px; border-radius:999px; color:#E2E8F0; font-size:0.82rem; font-weight:600; display:flex; align-items:center; gap:6px;">
                <span>🔒</span> Encrypted Biometric Vectors
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    footer_home()
