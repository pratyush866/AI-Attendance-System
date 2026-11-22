import streamlit as st
import os
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.ui.image_utils import get_image_base64

def home_screen():
    style_background_home()
    style_base_layout()
    header_home()

    # Load images with robust fallback
    student_img_b64 = None
    teacher_img_b64 = None

    if os.path.exists("assets/student_new.png"):
        student_img_b64 = get_image_base64("assets/student_new.png")
    elif os.path.exists("student.png"):
        student_img_b64 = get_image_base64("student.png")

    if os.path.exists("assets/teacher_new.png"):
        teacher_img_b64 = get_image_base64("assets/teacher_new.png")
    elif os.path.exists("snap-teacher.png"):
        teacher_img_b64 = get_image_base64("snap-teacher.png")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 12px;">
                <span style="background: #e0e7ff; color: #4338ca; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;">
                    🎓 STUDENT ACCESS
                </span>
                <h2 style="color: #0f172a; font-size: 1.85rem; font-weight: 800; margin: 10px 0 4px 0; font-family: 'Outfit', sans-serif;">
                    I'm a Student
                </h2>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0 0 12px 0;">
                    Live in-class selfie check-in & records
                </p>
                <div style="display: flex; justify-content: center; margin: 10px 0 16px 0;">
                    <img src="{student_img_b64}" style="width: 135px; height: 135px; object-fit: cover; border-radius: 50%; border: 4px solid #6366f1; box-shadow: 0 12px 24px -6px rgba(99, 102, 241, 0.35);" />
                </div>
                <div style="display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin-bottom: 18px;">
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 10px; border-radius: 8px; font-weight: 600;">📸 FaceID Login</span>
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 10px; border-radius: 8px; font-weight: 600;">⚡ Live Check-in</span>
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 10px; border-radius: 8px; font-weight: 600;">📊 Class Stats</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown(f"""
            <div style="text-align: center; margin-bottom: 12px;">
                <span style="background: #fce7f3; color: #be185d; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px;">
                    👨‍🏫 FACULTY PORTAL
                </span>
                <h2 style="color: #0f172a; font-size: 1.85rem; font-weight: 800; margin: 10px 0 4px 0; font-family: 'Outfit', sans-serif;">
                    I'm a Teacher
                </h2>
                <p style="color: #64748b; font-size: 0.9rem; margin: 0 0 12px 0;">
                    Start class sessions & Anti-bunk verification
                </p>
                <div style="display: flex; justify-content: center; margin: 10px 0 16px 0;">
                    <img src="{teacher_img_b64}" style="width: 135px; height: 135px; object-fit: cover; border-radius: 50%; border: 4px solid #ec4899; box-shadow: 0 12px 24px -6px rgba(236, 72, 153, 0.35);" />
                </div>
                <div style="display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin-bottom: 18px;">
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 10px; border-radius: 8px; font-weight: 600;">🚀 Start Session</span>
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 10px; border-radius: 8px; font-weight: 600;">🛡️ Anti-Bunk Match</span>
                    <span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 10px; border-radius: 8px; font-weight: 600;">📋 Export Reports</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
