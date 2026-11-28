import streamlit as st
from src.database.db import create_attendance, close_attendance_session

def show_attendance_result(df, logs, session_id=None):
    st.write('Please review the attendance results before confirming. You can see physical verification status below:')
    st.dataframe(df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', use_container_width=True):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('Confirm & Save Final Attendance', use_container_width=True, type='primary'):
            try:
                create_attendance(logs)
                if session_id:
                    close_attendance_session(session_id)
                    for k in list(st.session_state.keys()):
                        if k.startswith("active_session_"):
                            sess = st.session_state.get(k)
                            if isinstance(sess, dict) and sess.get("session_id") == session_id:
                                del st.session_state[k]
                st.success("✅ Attendance successfully saved to database!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f'Sync failed: {e}')

@st.dialog("📋 Final Attendance Verification Report")
def attendance_result_dialog(df, logs, session_id=None):
    show_attendance_result(df, logs, session_id=session_id)
