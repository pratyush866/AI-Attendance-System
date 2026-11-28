import streamlit as st
import numpy as np
from PIL import Image
from src.database.db import (
    get_session_by_id, 
    get_subject_students, 
    submit_session_selfie,
    get_session_selfies,
    create_student,
    enroll_student_to_subject,
    update_student_face_embedding
)
from src.pipelines.face_pipeline import (
    get_face_embeddings, 
    verify_student_selfie
)
from src.ui.base_layout import style_base_layout, style_background_dashboard

def session_checkin_screen(session_id):
    style_background_dashboard()
    style_base_layout()

    session = get_session_by_id(session_id)
    if not session:
        st.error("❌ Invalid or expired attendance link. Please ask your teacher for a new link.")
        if st.button("⬅️ Go to Home"):
            st.query_params.clear()
            st.rerun()
        return

    if session.get("status") == "closed":
        st.warning("⚠️ This attendance session has already been closed by the teacher.")
        if st.button("⬅️ Go to Home"):
            st.query_params.clear()
            st.rerun()
        return

    # Header Card
    st.markdown(f"""
        <div style="background: #ffffff; border-radius: 18px; padding: 20px; border: 1px solid #e2e8f0; border-left: 6px solid #4f46e5; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(0,0,0,0.04);">
            <div style="display: inline-block; background: #e0e7ff; color: #4338ca; padding: 3px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; margin-bottom: 8px;">
                ⚡ LIVE IN-CLASS ATTENDANCE
            </div>
            <h2 style="color: #0f172a; margin: 0; font-size: 1.5rem; font-weight: 800; font-family: 'Outfit', sans-serif;">{session['subject_name']}</h2>
            <p style="color: #64748b; margin: 6px 0 0 0; font-size: 0.95rem;">
                <b>Code:</b> <span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; color: #1e293b;">{session['subject_code']}</span> &nbsp;|&nbsp; 
                <b>Section:</b> {session['section']} &nbsp;|&nbsp; 
                <b>Teacher:</b> {session['teacher_name']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Fetch enrolled students
    enrolled_data = get_subject_students(session['subject_id'])
    enrolled_students = [item['students'] for item in enrolled_data if item.get('students')]

    # Check already submitted
    submitted_selfies = get_session_selfies(session_id)
    submitted_ids = [s['student_id'] for s in submitted_selfies]

    st.markdown("""
        <h3 style="color: #0f172a; margin: 15px 0 6px 0; font-size: 1.2rem; font-weight: 700;">
            Step 1: Identify Yourself & Enter Classroom PIN
        </h3>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if enrolled_students:
            student_options = {
                f"{s.get('roll_no') or s['student_id']} - {s['name']}": s
                for s in enrolled_students
            }
            student_options["➕ New Student (Not Enrolled)"] = None
            selected_label = st.selectbox("Select Your Roll No & Name", options=list(student_options.keys()))
            selected_student = student_options[selected_label]
        else:
            selected_student = None
            st.info("No students enrolled yet in this subject. You can register below.")

        if selected_student is None:
            new_student_name = st.text_input("Enter Your Full Name", placeholder="e.g. Rahul Sharma")
            new_student_roll = st.text_input("Enter Your Roll Number", placeholder="e.g. 101")

    with col2:
        entered_pin = st.text_input(
            "Enter 4-Digit Classroom PIN",
            max_chars=4,
            type="password",
            placeholder="Announced on blackboard"
        )
        st.caption("🔒 Confirms you are physically inside the room.")

    # Check if already submitted
    if selected_student and selected_student['student_id'] in submitted_ids:
        st.success(f"✅ Hello {selected_student['name']}, your live in-class selfie is ALREADY submitted for this session!")
        st.info("🕒 Please remain seated while the teacher takes the classroom verification photo.")
        return

    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 16px 0;'/>", unsafe_allow_html=True)
    st.markdown("""
        <h3 style="color: #0f172a; margin: 0 0 4px 0; font-size: 1.2rem; font-weight: 700;">
            Step 2: Take Live In-Class Selfie
        </h3>
        <p style="color: #64748b; margin: 0 0 12px 0; font-size: 0.9rem;">
            📸 Position your face clearly. Live camera only (gallery uploads disabled).
        </p>
    """, unsafe_allow_html=True)

    selfie_source = st.camera_input("Capture Live Selfie", key="student_session_camera")

    if selfie_source:
        if entered_pin.strip() != str(session['session_pin']).strip():
            st.error("❌ Incorrect Classroom PIN! Please check the 4-digit PIN written on the blackboard.")
            return

        with st.spinner("AI is verifying your face and presence..."):
            img_np = np.array(Image.open(selfie_source))
            
            # Handle new student registration on the fly
            if selected_student is None:
                if not new_student_name.strip():
                    st.warning("Please enter your name above.")
                    return
                encodings = get_face_embeddings(img_np)
                if not encodings:
                    st.error("❌ No face detected in your photo! Please face the camera properly with good light.")
                    return
                face_emb = encodings[0].tolist()
                created = create_student(
                    new_student_name.strip(),
                    roll_no=new_student_roll.strip() if new_student_roll.strip() else None,
                    face_embedding=face_emb
                )
                if created:
                    new_student = created[0]
                    enroll_student_to_subject(new_student['student_id'], session['subject_id'])
                    selected_student = new_student
                else:
                    st.error("Failed to register student profile. Please try again.")
                    return

            # Verification for existing registered student
            reg_emb = selected_student.get('face_embedding')
            is_valid, is_match, score_or_msg = verify_student_selfie(img_np, reg_emb)

            if not is_valid:
                st.error(f"⚠️ {score_or_msg}")
                return

            if not is_match:
                st.error(f"❌ Face Verification Failed: {score_or_msg}")
                st.warning("Your selfie does not match the registered face for this student ID!")
                return

            # If student had no previous face embedding, save this one
            if not reg_emb:
                encs = get_face_embeddings(img_np)
                if encs:
                    update_student_face_embedding(selected_student['student_id'], encs[0].tolist())

            # Record session selfie submission
            success = submit_session_selfie(
                session_id=session_id,
                student_id=selected_student['student_id'],
                similarity_score=float(score_or_msg) if isinstance(score_or_msg, (int, float)) else 1.0
            )

            if success:
                st.balloons()
                st.success(f"🎉 Live In-Class Selfie Verified for {selected_student['name']}!")
                st.markdown("""
                    <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 14px; padding: 16px; margin-top: 14px;">
                        <h4 style="color: #15803d; margin: 0; font-size: 1.1rem; font-weight: 700;">✅ Step 1 Completed!</h4>
                        <p style="color: #166534; margin: 6px 0 0 0; font-size: 0.95rem;">
                            Your in-class check-in is recorded. The teacher will now take a wide-angle photo of the room 
                            to cross-verify your physical presence. 
                            <br/><b>Anti-Bunk Security:</b> Attendance is finalized when both your selfie and classroom photo match.
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Failed to record check-in. Please try again.")
