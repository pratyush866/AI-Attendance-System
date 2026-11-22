import streamlit as st
from src.database.db import enroll_student_to_subject, get_subject_by_code, check_enrollment_exists
import time

def clear_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass

@st.dialog("Quick Enrollment ⚡")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.get('student_data', {}).get('student_id')
    if not student_id:
        st.error('Student session not found. Please login again.')
        return

    subjects_found = get_subject_by_code(subject_code)
    if not subjects_found:
        st.error('Subject Code not found!')
        if st.button('Close'):
            clear_query_params()
            st.rerun()
        return

    subject = subjects_found[0]
    if check_enrollment_exists(student_id, subject['subject_id']):
        st.info('You are already enrolled!')
        if st.button('Got it!'):
            clear_query_params()
            st.rerun()
        return

    st.write(f"Would you like to enroll in {subject['name']} ({subject['subject_code']})?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button('No, Discard', use_container_width=True):
            clear_query_params()
            st.rerun()
    with col2:
        if st.button('Yes, Enroll Now', type='primary', use_container_width=True):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success('Joined successfully!')
            clear_query_params()
            time.sleep(1)
            st.rerun()