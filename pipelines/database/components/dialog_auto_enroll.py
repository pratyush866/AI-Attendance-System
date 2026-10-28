import streamlit as st
from pipelines.database.db import (
    enroll_student_to_subject,
    get_subject_by_code,
    is_student_enrolled_in_subject
)
import time

def clear_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.get('student_data', {}).get('student_id')
    if not student_id:
        st.error('Student session not found. Please login again.')
        return

    subject = get_subject_by_code(subject_code)
    if not subject:
        st.error(f'Subject with code "{subject_code}" not found!')
        if st.button('Close'):
            clear_query_params()
            st.rerun()
        return

    if is_student_enrolled_in_subject(student_id, subject['subject_id']):
        st.info(f"You are already enrolled in {subject['name']}!")
        if st.button('Got it!'):
            clear_query_params()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject['name']}** (`{subject['subject_code']}`)?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            clear_query_params()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', use_container_width=True):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success(f"Joined {subject['name']} successfully!")
            clear_query_params()
            time.sleep(1)
            st.rerun()