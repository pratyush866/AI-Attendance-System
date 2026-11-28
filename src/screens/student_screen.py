import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image
import time

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
    roll_sort_key
)


def _parse_dt(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00").split(".")[0])
    except Exception:
        return None


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    roll_no = student_data.get('roll_no') or f"ID-{student_id}"

    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align: right;">
                <h3 style="color: #0f172a; margin: 0 0 4px 0; font-size: 1.35rem; font-weight: 700;">
                    👋 Welcome, <span style="color: #4f46e5;">{student_data['name']}</span>
                </h3>
                <div style="margin-bottom: 6px;">
                    <span style="background: #e0e7ff; color: #4338ca; padding: 3px 10px; border-radius: 9999px; font-size: 0.78rem; font-weight: 700;">
                        🎓 Roll No: {roll_no}
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type='secondary', key='student_logout_btn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    with st.spinner('Loading your attendance & enrolled subjects...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    # Overall KPI Strip
    total_all = len(logs)
    attended_all = sum(1 for lg in logs if lg.get('is_present'))
    overall_pct = round((attended_all / total_all) * 100, 1) if total_all > 0 else 0.0
    standing_lbl = "🟢 Safe (>= 75%)" if (total_all == 0 or overall_pct >= 75.0) else "⚠️ Shortage (< 75%)"

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("📊 Overall Attendance", f"{overall_pct:.1f}%")
    with k2:
        st.metric("✅ Present Classes", attended_all)
    with k3:
        st.metric("📅 Total Classes", total_all)
    with k4:
        st.metric("🎯 Eligibility Status", standing_lbl)

    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 14px 0;'/>", unsafe_allow_html=True)

    col_head_1, col_head_2 = st.columns([3, 2], vertical_alignment='center')
    with col_head_1:
        st.markdown("""
            <h2 style="color: #0f172a; margin: 0; font-size: 1.55rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
                📚 Your Enrolled Subjects
            </h2>
        """, unsafe_allow_html=True)
    with col_head_2:
        if st.button('➕ Enroll in New Subject', type='primary', use_container_width=True):
            enroll_dialog()

    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 12px 0;'/>", unsafe_allow_html=True)

    stats_map = {}
    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    if not subjects:
        st.info("You haven't enrolled in any subjects yet. Click '➕ Enroll in New Subject' above using the Subject Code provided by your teacher.")
    else:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']
            stats = stats_map.get(sid, {"total": 0, "attended": 0})
            sub_pct = round((stats['attended'] / stats['total']) * 100, 1) if stats['total'] > 0 else 0.0

            def unenroll_button(s_name=sub['name'], s_id=sid):
                st.markdown('<div class="tertiary-btn">', unsafe_allow_html=True)
                clicked = st.button(
                    f"Unenroll from {s_name}",
                    type='secondary',
                    key=f"unenroll_{s_id}",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
                if clicked:
                    unenroll_student_to_subject(student_id, s_id)
                    st.toast(f"Unenrolled from {s_name} successfully!")
                    st.rerun()

            with cols[i % 2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('📅', 'Total Classes', stats['total']),
                        ('✅', 'Attended', stats['attended']),
                        ('📈', 'Percentage', f"{sub_pct:.1f}%"),
                    ],
                    footer_callback=unenroll_button
                )

    # =========================================================================
    # MONTH-WISE ATTENDANCE PERCENTAGE BREAKDOWN & DATE-WISE LOG
    # =========================================================================
    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 20px 0 14px 0;'/>", unsafe_allow_html=True)
    st.markdown("""
        <h2 style="color: #0f172a; margin: 0 0 4px 0; font-size: 1.55rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
            📆 Month-Wise Attendance Percentage
        </h2>
        <p style="color: #64748b; margin: 0 0 12px 0; font-size: 0.9rem;">
            Track your monthly attendance percentage across all subjects or filter by a single subject.
        </p>
    """, unsafe_allow_html=True)

    if not logs:
        st.info("No classes have been recorded for you yet. Once your teacher saves attendance, your month-wise percentage will appear here automatically.")
    else:
        sub_filter_opts = ["All Subjects"] + sorted({
            f"{lg['subjects']['name']} ({lg['subjects']['subject_code']})"
            for lg in logs if lg.get('subjects')
        })
        chosen_sub_filter = st.selectbox("Filter by Subject", options=sub_filter_opts, key="stu_month_sub_filter")

        filtered_logs = [
            lg for lg in logs
            if chosen_sub_filter == "All Subjects"
            or (lg.get('subjects') and f"{lg['subjects']['name']} ({lg['subjects']['subject_code']})" == chosen_sub_filter)
        ]

        monthly_buckets = {}
        history_rows = []
        for lg in filtered_logs:
            dt = _parse_dt(lg.get('timestamp'))
            is_p = bool(lg.get('is_present'))
            if dt:
                m_key = dt.strftime("%Y-%m")
                m_label = dt.strftime("%B %Y")
                date_str = dt.strftime("%d %b %Y, %I:%M %p")
            else:
                m_key = "0000-00"
                m_label = "Unknown"
                date_str = "N/A"

            if m_key not in monthly_buckets:
                monthly_buckets[m_key] = {"Month": m_label, "Present": 0, "Absent": 0, "Total": 0}
            monthly_buckets[m_key]["Total"] += 1
            if is_p:
                monthly_buckets[m_key]["Present"] += 1
            else:
                monthly_buckets[m_key]["Absent"] += 1

            sub_info = lg.get('subjects') or {}
            history_rows.append({
                "_ts": str(lg.get('timestamp') or ''),
                "Date & Time": date_str,
                "Subject": sub_info.get('name', '-'),
                "Code": sub_info.get('subject_code', '-'),
                "Mark": "✔ Present" if is_p else "✘ Absent",
                "Verification": lg.get('verification_status', 'Verified')
            })

        month_rows = []
        for m_key in sorted(monthly_buckets.keys(), reverse=True):
            b = monthly_buckets[m_key]
            pct = round((b["Present"] / b["Total"]) * 100, 1) if b["Total"] > 0 else 0.0
            month_rows.append({
                "Month": b["Month"],
                "Total Classes": b["Total"],
                "✔ Present": b["Present"],
                "✘ Absent": b["Absent"],
                "Attendance %": pct,
                "Status": "✅ Safe (>=75%)" if pct >= 75.0 else "⚠️ Shortage (<75%)"
            })

        month_df = pd.DataFrame(month_rows)
        st.dataframe(
            month_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Attendance %": st.column_config.ProgressColumn(
                    "Attendance %",
                    format="%.1f%%",
                    min_value=0.0,
                    max_value=100.0
                )
            }
        )

        with st.expander("📋 View Date-Wise Attendance Log"):
            hist_df = pd.DataFrame(history_rows).sort_values(by="_ts", ascending=False)[
                ["Date & Time", "Subject", "Code", "Mark", "Verification"]
            ]
            st.dataframe(hist_df, use_container_width=True, hide_index=True)

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("⬅️ Home", type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
        <div style="text-align: center; margin: 15px 0 20px 0;">
            <h2 style="color: #0f172a; margin: 0; font-size: 1.8rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
                Student Portal
            </h2>
            <p style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">
                Authenticate with your FaceID or select your profile below.
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab_face, tab_select = st.tabs(["📸 FaceID Scanner", "📋 Quick Profile Login"])

    show_registration = False
    registered_photo_np = None

    with tab_face:
        photo_source = st.camera_input("Position your face in the center", key="student_face_login_cam")

        if photo_source:
            registered_photo_np = np.array(Image.open(photo_source))
            all_students = get_all_students()

            with st.spinner('AI Face Scanner is matching your profile...'):
                detected, all_ids, num_faces = predict_attendance(registered_photo_np, candidate_students=all_students)

                if num_faces == 0:
                    st.warning('Face not detected! Please ensure proper lighting and face the camera directly.')
                elif num_faces > 1:
                    st.warning('Multiple faces detected! Please ensure only you are in frame.')
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        student = next((s for s in all_students if str(s['student_id']) == str(student_id)), None)
                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            st.toast(f"Welcome Back, {student['name']}!")
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.info('Face not recognized! You can register your face profile below.')
                        show_registration = True

    with tab_select:
        all_students = sorted(get_all_students(), key=roll_sort_key)
        if all_students:
            s_map = {
                f"Roll {s.get('roll_no') or s['student_id']} — {s['name']}": s
                for s in all_students
            }
            selected_s_label = st.selectbox("Select Your Student Profile (Roll No. Sorted)", options=list(s_map.keys()))
            if st.button("Login as Student", type="primary", use_container_width=True):
                s_obj = s_map[selected_s_label]
                st.session_state.is_logged_in = True
                st.session_state.user_role = 'student'
                st.session_state.student_data = s_obj
                st.toast(f"Welcome Back, {s_obj['name']}!")
                time.sleep(0.5)
                st.rerun()
        else:
            st.info("No students registered yet. Please use the FaceID Scanner to register.")

    if show_registration and registered_photo_np is not None:
        with st.container(border=True):
            st.markdown("""
                <h3 style="color: #0f172a; margin-top: 0; font-weight: 700;">Register New Student Profile</h3>
            """, unsafe_allow_html=True)
            new_name = st.text_input("Enter Your Full Name", placeholder='e.g. Akash Sharma')
            new_roll = st.text_input("Enter Roll Number / Student ID", placeholder='e.g. 101')
            st.caption("Optional : Voice Enrollment for voice attendance")
            audio_data = None
            try:
                audio_data = st.audio_input('Record a short phrase (e.g. "I am present")')
            except Exception:
                pass

            if st.button('Create Profile & Enroll Face', type='primary', use_container_width=True):
                if new_name.strip():
                    with st.spinner('Extracting facial features and creating profile...'):
                        encodings = get_face_embeddings(registered_photo_np)
                        if encodings:
                            face_emb = encodings[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(
                                new_name=new_name.strip(),
                                roll_no=new_roll.strip() if new_roll else None,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )
                            if response_data:
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.balloons()
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Could not capture clear facial features. Please try with better lighting.")
                else:
                    st.warning('Please enter your full name!')

    footer_dashboard()
