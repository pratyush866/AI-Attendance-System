import streamlit as st
from PIL import Image
import time


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write('Add classroom photos to scan for attendance')

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        if st.session_state.photo_tab == 'camera':
            clicked_cam = st.button('Camera', type='primary', use_container_width=True)
        else:
            st.markdown('<div class="tertiary-btn">', unsafe_allow_html=True)
            clicked_cam = st.button('Camera', type='secondary', use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if clicked_cam:
            st.session_state.photo_tab = 'camera'

    with t2:
        if st.session_state.photo_tab == 'upload':
            clicked_upload = st.button('Upload photos', type='primary', use_container_width=True)
        else:
            st.markdown('<div class="tertiary-btn">', unsafe_allow_html=True)
            clicked_upload = st.button('Upload photos', type='secondary', use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        if clicked_upload:
            st.session_state.photo_tab = 'upload'

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.success('Photo Captured')
            st.rerun()


    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader( 'choose image files', type=['jpg', 'png', 'jpeg' ], accept_multiple_files=True, key='dialog_upload')

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            
            st.success('Photo Uploaded Successfully')
            st.rerun()

    st.divider()
    if st.button('Done', type='primary', use_container_width=True):
        st.rerun()