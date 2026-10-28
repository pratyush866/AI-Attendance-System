import streamlit as st
from pipelines.database.db import (
    enroll_student_to_subject,
    get_subject_by_code,
    is_student_enrolled_in_subject
)
import time

@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101').strip()

    if st.button('Enroll now', type='primary', use_container_width=True):
        if join_code:
            subject = get_subject_by_code(join_code)
            if subject:
                student_id = st.session_state.student_data['student_id']
                if is_student_enrolled_in_subject(student_id, subject['subject_id']):
                    st.warning('You are already enrolled in this subject')
                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success(f"Successfully enrolled in {subject['name']}!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Invalid Subject Code. Please check with your teacher.")
        else:
            st.warning('Please enter a subject code')