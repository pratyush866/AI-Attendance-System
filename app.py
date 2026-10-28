import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from pipelines.database.components.dialog_auto_enroll import auto_enroll_dialog

# Configure page settings
st.set_page_config(
    page_title="SnapClass - AI Attendance System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Handle QR code / Join Link query parameter
    join_code = st.query_params.get("join-code")
    if join_code:
        # If user opens a join link, direct to student portal
        if "login_type" not in st.session_state or st.session_state.login_type != "student":
            st.session_state["login_type"] = "student"

    # Initialize navigation routing
    if "login_type" not in st.session_state or st.session_state.login_type is None:
        home_screen()
    elif st.session_state.login_type == "student":
        student_screen()
        # If student is logged in and accessed via join link, trigger auto enroll dialog
        if join_code and st.session_state.get("student_data"):
            auto_enroll_dialog(join_code)
    elif st.session_state.login_type == "teacher":
        teacher_screen()
    else:
        st.session_state.login_type = None
        home_screen()

if __name__ == "__main__":
    main()