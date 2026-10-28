import streamlit as st

from src.screens.UI.base_layout import style_background_dashboard, style_base_layout

from pipelines.database.components.header import header_dashboard
from pipelines.database.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from pipelines.voice_pipeline import get_voice_embedding, identify_speaker
from pipelines.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject, update_student
import time

from pipelines.database.components.dialog_enroll import enroll_dialog
from pipelines.database.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns([3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        roll = student_data.get('roll_number')
        roll_badge = f"<span style='font-size:0.82rem; color:#4F46E5; background:#EEF2FF; border:1px solid #C7D2FE; padding:3px 10px; border-radius:6px; margin-left:8px; vertical-align:middle; font-weight:700;'>Roll No: {roll}</span>" if roll else ""
        st.markdown(f"<div style='text-align:right; margin-bottom:6px;'><span style='font-size:1.05rem; font-weight:700; color:#0F172A;'>{student_data['name']}</span>{roll_badge}</div>", unsafe_allow_html=True)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    tab_courses, tab_profile = st.tabs(["📚 My Courses", "👤 My Profile"])

    with tab_courses:
        c1, c2 = st.columns([2, 1], vertical_alignment='center')
        with c1:
            st.header('Your Enrolled Subjects')
        with c2:
            if st.button('Enroll in Subject', type='primary', use_container_width=True):
                enroll_dialog()

        st.divider()

        with st.spinner('Loading your enrolled subjects..'):
            subjects = get_student_subjects(student_id)
            logs = get_student_attendance(student_id)

        stats_map = {}
        for log in logs:
            sid = log['subject_id']
            if sid not in stats_map:
                stats_map[sid] = {"total": 0, "attended": 0}
            stats_map[sid]['total'] += 1
            if log.get('is_present'):
                stats_map[sid]['attended'] += 1

        # Calculate Statistics
        total_subjects = len(subjects)
        total_classes = sum(s['total'] for s in stats_map.values())
        total_attended = sum(s['attended'] for s in stats_map.values())
        overall_attendance = (total_attended / total_classes * 100) if total_classes > 0 else 100.0

        # Stats Cards
        st.markdown("### Dashboard Summary")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Enrolled Courses", value=total_subjects)
        with m2:
            st.metric(label="Total Classes Recorded", value=total_classes)
        with m3:
            st.metric(label="Overall Attendance", value=f"{overall_attendance:.1f}%")

        st.divider()

        if total_subjects == 0:
            st.info("You are not enrolled in any subjects yet. Click 'Enroll in Subject' to begin!")
        else:
            cols = st.columns(2)
            for i, sub_node in enumerate(subjects):
                sub = sub_node.get('subjects')
                if not sub:
                    continue
                sid = sub.get('subject_id')
                stats = stats_map.get(sid, {"total": 0, "attended": 0})
                
                # Percentage calculation
                ratio = (stats['attended'] / stats['total']) if stats['total'] > 0 else 1.0
                pct = ratio * 100

                def unenroll_button(subject_name=sub['name'], subject_id=sid):
                    if st.button("Unenroll from this course", type='tertiary', use_container_width=True, icon=':material/delete_forever:', key=f"unenroll_{subject_id}"):
                        unenroll_student_to_subject(student_id, subject_id)
                        st.success(f'Unenrolled from {subject_name} successfully!')
                        time.sleep(1)
                        st.rerun()

                with cols[i % 2]:
                    subject_card(
                        name=sub['name'],
                        code=sub['subject_code'],
                        section=sub['section'],
                        stats=[
                            ('📅', 'Total Sessions', stats['total']),
                            ('✅', 'Attended', stats['attended']),
                        ],
                        footer_callback=unenroll_button
                    )
                    # Visual Progress Bar
                    st.progress(ratio)
                    # Attendance color indicator based on standard academic thresholds (75%)
                    if pct < 75.0 and stats['total'] > 0:
                        st.markdown(f"<div style='text-align:right; font-size:0.85rem; color:#ef4444; margin-top:-10px; margin-bottom:15px;'>Attendance: <b>{pct:.1f}%</b> (Low Attendance ⚠️)</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align:right; font-size:0.85rem; color:#10b981; margin-top:-10px; margin-bottom:15px;'>Attendance: <b>{pct:.1f}%</b></div>", unsafe_allow_html=True)

    with tab_profile:
        st.header("My Profile Details")
        st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
        
        prof_c1, prof_c2 = st.columns(2)
        with prof_c1:
            updated_name = st.text_input("Full Name", value=student_data['name'], placeholder="Full Name")
        with prof_c2:
            updated_roll = st.text_input("Roll Number / College ID", value=student_data.get('roll_number') or '', placeholder="E.g. 21CS042")
        
        st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
        st.subheader("Update Credentials")
        
        update_face = st.checkbox("Update Face Recognition ID")
        new_photo = None
        if update_face:
            st.info("Position your face in the center of the camera to update your face ID")
            new_photo = st.camera_input("Capture New Face ID", key="update_face_cam")
            
        update_voice = st.checkbox("Update Voice Recognition Pattern")
        new_voice = None
        if update_voice:
            st.info("Record a short voice sample to update your voice print")
            new_voice = st.audio_input("Record Voice Sample", key="update_voice_rec")
            if new_voice:
                st.success("Voice sample ready for saving!")

        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
        if st.button("Save Profile Updates", type="primary", use_container_width=True):
            if not updated_name.strip():
                st.error("Name field cannot be left blank!")
            else:
                with st.spinner("Syncing updates with database..."):
                    face_emb = None
                    if update_face:
                        if new_photo:
                            img = np.array(Image.open(new_photo))
                            encodings = get_face_embeddings(img)
                            if encodings:
                                face_emb = encodings[0].tolist()
                            else:
                                st.error("No face detected in the snapshot. Please retry face capture.")
                                st.stop()
                        else:
                            st.warning("Please capture a photo to update your Face ID!")
                            st.stop()

                    voice_emb = None
                    if update_voice:
                        if new_voice:
                            voice_emb = get_voice_embedding(new_voice.getvalue())
                        else:
                            st.warning("Please record a voice sample to update your Voice ID!")
                            st.stop()

                    # Save to db
                    res = update_student(
                        student_id, 
                        updated_name.strip(), 
                        roll_number=updated_roll.strip() if updated_roll.strip() else None,
                        face_embedding=face_emb, 
                        voice_embedding=voice_emb
                    )
                    if res:
                        if face_emb:
                            train_classifier()
                        st.session_state.student_data = res[0]
                        st.success("Profile and biometrics updated successfully!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to update profile. Please try again.")

    footer_dashboard()

def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1, c2 = st.columns([3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    pad1, center_col, pad2 = st.columns([1, 2.2, 1])
    with center_col:
        # Login / Register Navigation Tabs
        if 'student_mode' not in st.session_state:
            st.session_state.student_mode = 'login'

        t1, t2 = st.columns(2)
        with t1:
            btn_type = 'primary' if st.session_state.student_mode == 'login' else 'tertiary'
            if st.button('Login (Biometrics)', type=btn_type, use_container_width=True, icon=':material/lock_open:'):
                st.session_state.student_mode = 'login'
                st.rerun()
        with t2:
            btn_type = 'primary' if st.session_state.student_mode == 'register' else 'tertiary'
            if st.button('Register Profile', type=btn_type, use_container_width=True, icon=':material/person_add:'):
                st.session_state.student_mode = 'register'
                st.rerun()

        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

        if st.session_state.student_mode == 'login':
            st.markdown("""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:1.8rem 2rem; box-shadow:0 10px 30px -5px rgba(0,0,0,0.05); margin-bottom:1.5rem;">
                    <h3 style='text-align: center; margin:0 0 6px 0; color:#0F172A;'>Biometric Student Login</h3>
                    <p style='text-align: center; color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;'>Authenticate touchlessly using your Face ID or Voice ID</p>
            """, unsafe_allow_html=True)
            
            login_method = st.radio("Select Login Method", ["📸 Face ID", "🎙️ Voice ID"], horizontal=True)

            if login_method == "📸 Face ID":
                photo_source = st.camera_input("Position your face in the center")

                if photo_source:
                    img = np.array(Image.open(photo_source))

                    with st.spinner('AI is scanning face...'):
                        detected, all_ids, num_faces = predict_attendance(img)

                        if num_faces == 0:
                            st.warning('Face not found!')
                        elif num_faces > 1:
                            st.warning('Multiple faces found. Please ensure only one person is in frame.')
                        else:
                            if detected:
                                student_id = list(detected.keys())[0]
                                all_students = get_all_students()
                                student = next((s for s in all_students if s['student_id'] == student_id), None)

                                if student:
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = student
                                    st.success(f"Welcome Back, {student['name']}! 👋")
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.info('Face not recognized! You might be a new student. Register below or switch to Register tab.')
                                if st.button('Switch to Register Profile', type='primary', use_container_width=True):
                                    st.session_state.student_mode = 'register'
                                    st.rerun()
            else:
                st.info('Record a phrase (e.g. "I am present") to log in with your Voice ID')
                voice_source = st.audio_input("Speak into the microphone")

                if voice_source:
                    with st.spinner('AI is analyzing voiceprint...'):
                        voice_emb = get_voice_embedding(voice_source.getvalue())
                        if not voice_emb:
                            st.warning("Could not extract voice features. Please speak clearly for at least 1-2 seconds.")
                        else:
                            all_students = get_all_students()
                            candidates = {s['student_id']: s.get('voice_embedding') for s in all_students if s.get('voice_embedding')}
                            
                            if not candidates:
                                st.error("No registered voice profiles found in the system. Please register first.")
                            else:
                                matched_sid, score = identify_speaker(voice_emb, candidates, threshold=0.60)
                                if matched_sid:
                                    student = next((s for s in all_students if s['student_id'] == matched_sid), None)
                                    if student:
                                        st.session_state.is_logged_in = True
                                        st.session_state.user_role = 'student'
                                        st.session_state.student_data = student
                                        st.success(f"Voice Verified! (Confidence: {score*100:.1f}%). Welcome, {student['name']}! 👋")
                                        time.sleep(1)
                                        st.rerun()
                                else:
                                    st.error("Voice not recognized. Please try speaking again or use Face ID.")
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.student_mode == 'register':
            st.markdown("""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:1.8rem 2rem; box-shadow:0 10px 30px -5px rgba(0,0,0,0.05); margin-bottom:1.5rem;">
                    <h3 style='text-align: center; margin:0 0 6px 0; color:#0F172A;'>Register Student Profile</h3>
                    <p style='text-align: center; color:#64748B; font-size:0.9rem; margin-bottom:1.5rem;'>Enroll your face and voice biometrics for touchless attendance</p>
            """, unsafe_allow_html=True)
            
            rc1, rc2 = st.columns(2)
            with rc1:
                new_name = st.text_input("Full Name *", placeholder='E.g. Pratyush Mishra')
            with rc2:
                new_roll = st.text_input("Roll Number / College ID *", placeholder='E.g. 21CS042')

            st.markdown("<h4 style='font-size:1.05rem; margin-top:10px;'>Face ID Capture (Required)</h4>", unsafe_allow_html=True)
            photo_source = st.camera_input("Position your face in the center", key="reg_cam_source")

            st.markdown("<h4 style='font-size:1.05rem; margin-top:14px;'>Voice Enrollment (Optional)</h4>", unsafe_allow_html=True)
            st.caption("Enroll your voice pattern to enable voice-only attendance & voice login")

            audio_data = None
            try:
                audio_data = st.audio_input('Record a phrase like "I am present, my name is..."')
            except Exception:
                st.error('Microphone setup failed!')

            if audio_data:
                st.success("🎙️ Voice sample recorded successfully!")

            st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)
            if st.button('Create Account →', type='primary', use_container_width=True):
                if not new_name.strip():
                    st.warning('Please enter your name!')
                elif not new_roll.strip():
                    st.warning('Please enter your Roll Number / College ID!')
                elif not photo_source:
                    st.warning('Please capture a face photo for registration!')
                else:
                    with st.spinner('Creating profile and extracting biometric vectors...'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.getvalue())

                            response_data = create_student(
                                new_name.strip(), 
                                roll_number=new_roll.strip(),
                                face_embedding=face_emb, 
                                voice_embedding=voice_emb
                            )

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.success(f'Profile Created Successfully! Welcome, {new_name} ({new_roll.strip()})!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Could not extract facial features. Ensure face is centered and clearly visible.')
            st.markdown("</div>", unsafe_allow_html=True)
        
    footer_dashboard()