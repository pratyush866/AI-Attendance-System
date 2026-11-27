import os
import streamlit as st
import importlib

# Reload submodules so changes reflect immediately without caching
import src.ui.base_layout
import src.ui.image_utils
import src.components.header
import src.components.footer
import src.screens.home_screen
import src.screens.teacher_screen
import src.screens.student_screen
import src.screens.session_checkin_screen
import src.components.dialog_auto_enroll

importlib.reload(src.ui.base_layout)
importlib.reload(src.ui.image_utils)
importlib.reload(src.components.header)
importlib.reload(src.components.footer)
importlib.reload(src.screens.home_screen)
importlib.reload(src.screens.teacher_screen)
importlib.reload(src.screens.student_screen)
importlib.reload(src.screens.session_checkin_screen)
importlib.reload(src.components.dialog_auto_enroll)

# Custom spacer function to resolve st.space() calls
if not hasattr(st, "space"):
    def space():
        st.markdown("<div style='padding: 5px 0;'></div>", unsafe_allow_html=True)
    st.space = space
 
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.screens.session_checkin_screen import session_checkin_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    icon = "assets/student_new.png" if os.path.exists("assets/student_new.png") else "🎓"
    st.set_page_config(
        page_title='AI Attendance System | Orbitals team',
        page_icon=icon,
        layout='centered'
    )

    # Route: Check if a student opened an in-class live attendance link
    session_param = st.query_params.get('session')
    if session_param:
        session_checkin_screen(session_param)
        return

    # Route: Check if join-code was provided for course enrollment
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.get('login_type') != 'student':
            st.session_state['login_type'] = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()
        
        case None:
            home_screen()

if __name__ == '__main__':
    main()
