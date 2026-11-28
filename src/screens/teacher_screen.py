import streamlit as st
import random
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists, 
    create_teacher, 
    teacher_login, 
    get_teacher_subjects, 
    get_attendance_for_teacher, 
    get_subject_students,
    create_attendance_session,
    get_active_session_for_subject,
    close_attendance_session,
    get_session_selfies,
    get_or_create_student_by_roll,
    enroll_student_to_subject,
    create_attendance,
    roll_sort_key
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_share_session import share_session_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.pipelines.face_pipeline import predict_attendance


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align: right;">
                <h3 style="color: #0f172a; margin: 0 0 6px 0; font-size: 1.4rem; font-weight: 700;">
                    👋 Welcome, <span style="color: #4f46e5;">{teacher_data['name']}</span>
                </h3>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type='secondary', key='teacher_logout_btn'):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type_btn = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'secondary'
        if st.button('⚡ Live Attendance', type=type_btn, use_container_width=True):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type_btn = 'primary' if st.session_state.current_teacher_tab == 'manage_subjects' else 'secondary'
        if st.button('📚 Manage Subjects', type=type_btn, use_container_width=True):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type_btn = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'secondary'
        if st.button('📊 Attendance Records', type=type_btn, use_container_width=True):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 15px 0 20px 0;'/>", unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.markdown("""
        <h2 style="color: #0f172a; margin: 0; font-size: 1.6rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
            ⚡ In-Class Dual-Verification Attendance
        </h2>
        <p style="color: #64748b; margin: 4px 0 16px 0; font-size: 0.95rem;">
            Anti-Bunk System: Combines student live in-class selfies with teacher classroom photo verification.
        </p>
    """, unsafe_allow_html=True)

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning('You have not created any subjects yet! Please create one in "Manage Subjects" to begin.')
        return

    subject_options = {f"{s['name']} - {s['subject_code']} ({s['section']})": s for s in subjects}
    selected_subject_label = st.selectbox('Select Subject / Class', options=list(subject_options.keys()))
    selected_subject = subject_options[selected_subject_label]
    selected_subject_id = selected_subject['subject_id']

    session_key = f"active_session_{selected_subject_id}"

    st.markdown("""
        <div style="margin: 18px 0 8px 0;">
            <h3 style="color: #0f172a; margin: 0; font-size: 1.25rem; font-weight: 700;">
                Step 1: Start In-Class Live Session
            </h3>
        </div>
    """, unsafe_allow_html=True)

    current_session = st.session_state.get(session_key)
    if not current_session:
        db_active = get_active_session_for_subject(selected_subject_id)
        if db_active:
            st.session_state[session_key] = db_active
            current_session = db_active

    col_sess_1, col_sess_2 = st.columns([3, 2], vertical_alignment='center')
    with col_sess_1:
        if not current_session:
            st.info("Start a live session to generate a student check-in link & Classroom PIN.")
        else:
            pin = current_session['session_pin']
            sid = current_session['session_id']
            st.markdown(f"""
                <div style="background: #ffffff; border: 2px solid #4f46e5; border-radius: 14px; padding: 14px 18px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);">
                    <div style="font-size: 1.05rem; color: #0f172a; font-weight: 600;">
                        🟢 <b>Session Active:</b> <code>{sid}</code> &nbsp;|&nbsp; 
                        <b>Classroom PIN:</b> <span style="background: #fef08a; padding: 3px 10px; border-radius: 6px; font-weight: 800; color: #854d0e;">{pin}</span>
                    </div>
                    <div style="color: #64748b; font-size: 0.88rem; margin-top: 5px;">
                        Write the PIN on the board. Students click the session link and upload their in-class selfie.
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with col_sess_2:
        if not current_session:
            if st.button("🚀 Start Live Session", type="primary", use_container_width=True):
                new_pin = random.randint(1000, 9999)
                sess = create_attendance_session(selected_subject_id, teacher_id, new_pin)
                st.session_state[session_key] = sess
                st.rerun()
        else:
            c_btn1, c_btn2, c_btn3 = st.columns([2, 1.4, 1.4])
            with c_btn1:
                if st.button("📲 Share QR", type="primary", use_container_width=True):
                    share_session_dialog(current_session['session_id'], current_session['session_pin'], selected_subject['name'])
            with c_btn2:
                if st.button("🔄 Refresh", use_container_width=True):
                    st.rerun()
            with c_btn3:
                if st.button("⏹️ End", use_container_width=True, key="end_live_sess_btn"):
                    close_attendance_session(current_session['session_id'])
                    del st.session_state[session_key]
                    st.rerun()

    # If session is active, show live submissions list
    if current_session:
        selfies = get_session_selfies(current_session['session_id'])
        enrolled_res = get_subject_students(selected_subject_id)
        total_enrolled = len(enrolled_res)

        st.markdown(f"""
            <div style="margin-top: 10px; color: #0f172a; font-weight: 600; font-size: 0.95rem;">
                👥 Live Student Selfies Submitted: <span style="color: #4f46e5; font-size: 1.1rem; font-weight: 800;">{len(selfies)} / {total_enrolled} Students</span>
            </div>
        """, unsafe_allow_html=True)
        if selfies:
            submitted_names = [f"✅ {s['student_name']}" for s in selfies]
            st.markdown(
                '<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 14px; font-size: 0.9rem; color: #1e293b; margin-top: 6px;">'
                + " &nbsp;•&nbsp; ".join(submitted_names)
                + '</div>',
                unsafe_allow_html=True
            )
        else:
            st.caption("Waiting for students in class to submit their selfie on the link...")

    st.markdown("""
        <div style="margin: 22px 0 8px 0;">
            <h3 style="color: #0f172a; margin: 0; font-size: 1.25rem; font-weight: 700;">
                Step 2: Take Classroom Wide Photo
            </h3>
            <p style="color: #64748b; margin: 2px 0 0 0; font-size: 0.9rem;">
                Take 1 or 2 wide-angle photos of the classroom to verify students physically sitting in the room.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')
    with col1:
        st.write(f"Classroom Photos Added: **{len(st.session_state.attendance_images)}**")
    with col2:
        if st.button('📸 Add Photos', type='primary', use_container_width=True):
            add_photos_dialog()

    if st.session_state.attendance_images:
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="tertiary-btn">', unsafe_allow_html=True)
        clear_clicked = st.button('🗑️ Clear photos', use_container_width=True, type='secondary', disabled=not has_photos)
        st.markdown('</div>', unsafe_allow_html=True)
        if clear_clicked:
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        btn_label = "🤖 Run Dual-Verification" if current_session else "🔍 Run Face Analysis"
        if st.button(btn_label, use_container_width=True, type='primary', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos & cross-matching with student selfies...'):
                enrolled_students = get_subject_students(selected_subject_id)
                if not enrolled_students:
                    st.warning('No students enrolled in this course!')
                    return

                candidates = sorted(
                    [node['students'] for node in enrolled_students if node.get('students')],
                    key=roll_sort_key
                )
                all_detected_ids = {}

                # Scan classroom photos
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np, candidate_students=candidates)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                # Fetch session selfies if active
                submitted_selfie_ids = set()
                session_id_val = None
                if current_session:
                    session_id_val = current_session['session_id']
                    selfies = get_session_selfies(session_id_val)
                    submitted_selfie_ids = {s['student_id'] for s in selfies}

                results, attendance_to_log = [], []
                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                for student in candidates:
                    sid = student['student_id']
                    in_photo = len(all_detected_ids.get(sid, [])) > 0
                    in_selfie = sid in submitted_selfie_ids

                    if current_session:
                        if in_photo and in_selfie:
                            status = "🟢 Verified Present"
                            is_present = True
                            verif_note = "Selfie + Photo Match (No Bunk)"
                        elif in_selfie and not in_photo:
                            status = "🔴 Bunk Alert!"
                            is_present = False
                            verif_note = "Selfie from outside! Missing in classroom"
                        elif in_photo and not in_selfie:
                            status = "🟡 In Photo (No Selfie)"
                            is_present = True
                            verif_note = "Face detected in room (phone issue)"
                        else:
                            status = "❌ Absent"
                            is_present = False
                            verif_note = "Not in class"
                    else:
                        status = "🟢 Present" if in_photo else "❌ Absent"
                        is_present = in_photo
                        verif_note = "Classroom Photo"

                    results.append({
                        "Roll No": student.get('roll_no') or f"ID-{sid}",
                        "Name": student['name'],
                        "In-Class Selfie": "✅ Yes" if in_selfie else "❌ No",
                        "Classroom Photo": "✅ Yes" if in_photo else "❌ No",
                        "Status": status,
                        "Present": bool(is_present),
                        "Security Note": verif_note
                    })

                    attendance_to_log.append({
                        'student_id': sid,
                        'subject_id': selected_subject_id,
                        'session_id': session_id_val or '',
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present),
                        'verification_status': status
                    })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log, session_id=session_id_val)

    with c3:
        if st.button('🎤 Voice Attendance', type='secondary', use_container_width=True):
            voice_attendance_dialog(selected_subject_id)

    # Quick Digital Roll-Call Fallback (no camera required)
    with st.expander("📋 Quick Digital Roll-Call (Manual / No-Camera Backup)"):
        enrolled_nodes = get_subject_students(selected_subject_id)
        roster = sorted(
            [n['students'] for n in enrolled_nodes if n.get('students')],
            key=roll_sort_key
        )
        if not roster:
            st.info("No students enrolled in this subject yet. Add students in 'Manage Subjects'.")
        else:
            st.caption("All students are automatically sorted by Roll No. Tick Present students and save directly to the register.")
            mark_all = st.checkbox("Select All Present", value=False, key=f"mark_all_{selected_subject_id}")
            manual_df = pd.DataFrame([
                {
                    "Roll No": s.get("roll_no") or f"ID-{s['student_id']}",
                    "Student Name": s["name"],
                    "Present": bool(mark_all),
                    "_sid": s["student_id"]
                }
                for s in roster
            ])
            edited_manual = st.data_editor(
                manual_df[["Roll No", "Student Name", "Present"]],
                hide_index=True,
                use_container_width=True,
                disabled=["Roll No", "Student Name"],
                column_config={
                    "Present": st.column_config.CheckboxColumn("Present (✔)", default=False)
                },
                key=f"manual_rollcall_{selected_subject_id}"
            )
            if st.button("💾 Save Digital Roll-Call to Register", type="primary", use_container_width=True, key=f"save_manual_{selected_subject_id}"):
                ts_now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                manual_logs = []
                for idx, s in enumerate(roster):
                    is_p = bool(edited_manual.iloc[idx]["Present"])
                    manual_logs.append({
                        "student_id": s["student_id"],
                        "subject_id": selected_subject_id,
                        "session_id": current_session["session_id"] if current_session else "",
                        "timestamp": ts_now,
                        "is_present": is_p,
                        "verification_status": "🟢 Present (Teacher Roll-Call)" if is_p else "❌ Absent"
                    })
                create_attendance(manual_logs)
                if current_session:
                    close_attendance_session(current_session["session_id"])
                    del st.session_state[session_key]
                st.success(f"✅ Saved attendance for {len(manual_logs)} students!")
                st.rerun()


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns([3, 2], vertical_alignment='center')
    with col1:
        st.markdown("""
            <h2 style="color: #0f172a; margin: 0; font-size: 1.6rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
                📚 Manage Subjects
            </h2>
        """, unsafe_allow_html=True)

    with col2:
        if st.button('➕ Create New Subject', use_container_width=True, type='primary'):
            create_subject_dialog(teacher_id)

    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 15px 0 20px 0;'/>", unsafe_allow_html=True)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            def share_btn(current_sub=sub):
                if st.button(f"📲 Share Code: {current_sub['name']}", key=f"share_{current_sub['subject_code']}", use_container_width=True):
                    share_subject_dialog(current_sub['name'], current_sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

        # Bulk Student Roster Setup (no manual student-by-student enrollment needed)
        st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 16px 0;'/>", unsafe_allow_html=True)
        with st.expander("👥 Add / Bulk Import Class Students (Roll No + Name)"):
            st.caption(
                "Paste your class list (one student per line as `RollNo, Student Name`) to add the full batch at once. "
                "Existing Roll Numbers are reused automatically across all subjects!"
            )
            roster_sub_map = {f"{s['name']} ({s['subject_code']} • {s['section']})": s['subject_id'] for s in subjects}
            target_sub_lbl = st.selectbox("Target Subject", options=list(roster_sub_map.keys()), key="bulk_target_sub")
            bulk_text = st.text_area(
                "Student List (Roll No, Name)",
                placeholder="2514018680026, Adesh Bhatt\n2514018680041, Atul Upadhyay\n2514018680045, Divyanshu Upadhyay\n2514018680055, Mo Ashad\n2514018680059, Pratyush Mishra",
                height=140,
                key="bulk_student_lines"
            )
            if st.button("➕ Add & Enroll Students", type="primary", use_container_width=True, key="bulk_enroll_btn"):
                lines = [ln.strip() for ln in bulk_text.splitlines() if ln.strip()]
                if not lines:
                    st.warning("Please enter at least one student line.")
                else:
                    target_sid = roster_sub_map[target_sub_lbl]
                    added_cnt, enrolled_cnt = 0, 0
                    for ln in lines:
                        if "," in ln:
                            parts = ln.split(",", 1)
                        elif "\t" in ln:
                            parts = ln.split("\t", 1)
                        elif " - " in ln:
                            parts = ln.split(" - ", 1)
                        else:
                            parts = ln.split(None, 1)
                        if len(parts) == 2:
                            r_no, s_name = parts[0].strip(), parts[1].strip()
                        else:
                            r_no, s_name = None, parts[0].strip()
                        if s_name:
                            stu, is_new = get_or_create_student_by_roll(s_name, r_no)
                            if stu:
                                if is_new:
                                    added_cnt += 1
                                enroll_student_to_subject(stu['student_id'], target_sid)
                                enrolled_cnt += 1
                    st.success(f"✅ Enrolled {enrolled_cnt} students ({added_cnt} newly created) sorted by Roll No!")
                    st.rerun()
    else:
        st.info("NO SUBJECTS FOUND. Click '➕ Create New Subject' above to get started.")


def _parse_iso_dt(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00").split(".")[0])
    except Exception:
        return None


def teacher_tab_attendance_records():
    st.markdown("""
        <h2 style="color: #0f172a; margin: 0; font-size: 1.6rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
            📊 Attendance Register & Monthly Reports
        </h2>
        <p style="color: #64748b; margin: 4px 0 12px 0; font-size: 0.92rem;">
            Roll No.-sorted date-wise classroom register with automatic ✔ Present / ✘ Absent marks.
        </p>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 1px solid #e2e8f0; margin: 8px 0 16px 0;'/>", unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data['teacher_id']
    subjects = get_teacher_subjects(teacher_id)
    records = get_attendance_for_teacher(teacher_id)

    if not subjects and not records:
        st.info("No subjects or attendance records found yet.")
        return

    # Filter bar: Subject + Month
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        if subjects:
            sub_map = {f"{s['name']} ({s['subject_code']} • {s['section']})": s for s in subjects}
            selected_sub_label = st.selectbox("Select Subject for Register", options=list(sub_map.keys()), key="reg_sub_select")
            selected_sub = sub_map[selected_sub_label]
            selected_sub_id = selected_sub['subject_id']
        else:
            selected_sub = None
            selected_sub_id = None

    sub_records = [r for r in records if selected_sub_id is None or r.get('subject_id') == selected_sub_id]

    month_map = {}
    for r in sub_records:
        dt = _parse_iso_dt(r.get('timestamp'))
        if dt:
            m_key = dt.strftime("%Y-%m")
            month_map[m_key] = dt.strftime("%B %Y")

    sorted_months = sorted(month_map.keys(), reverse=True)
    month_options = ["All Months"] + [month_map[m] for m in sorted_months]
    label_to_mkey = {month_map[m]: m for m in sorted_months}

    with f_col2:
        selected_month_label = st.selectbox("Filter by Month", options=month_options, key="reg_month_select")

    if selected_month_label != "All Months":
        target_mkey = label_to_mkey[selected_month_label]
        filtered_records = [
            r for r in sub_records
            if (_parse_iso_dt(r.get('timestamp')) and _parse_iso_dt(r.get('timestamp')).strftime("%Y-%m") == target_mkey)
        ]
    else:
        filtered_records = sub_records

    tab_reg, tab_sess = st.tabs(["📋 Date-Wise Register (Roll No. Sorted)", "📅 Session Summary & Logs"])

    with tab_reg:
        # Combine enrolled students + any students present in logs, sorted automatically by Roll No
        student_roster = {}
        if selected_sub_id is not None:
            for node in get_subject_students(selected_sub_id):
                stu = node.get('students')
                if stu:
                    student_roster[stu['student_id']] = {
                        'student_id': stu['student_id'],
                        'name': stu['name'],
                        'roll_no': stu.get('roll_no')
                    }

        for r in filtered_records:
            sid = r.get('student_id')
            if sid and sid not in student_roster:
                student_roster[sid] = {
                    'student_id': sid,
                    'name': r.get('student_name') or f"Student #{sid}",
                    'roll_no': r.get('roll_no')
                }

        sorted_roster = sorted(student_roster.values(), key=roll_sort_key)

        if not sorted_roster:
            st.info("No students enrolled in this subject yet.")
        elif not filtered_records:
            st.info("No attendance has been marked for this selection yet. Showing enrolled students sorted by Roll No:")
            empty_df = pd.DataFrame([
                {
                    "Roll No": s.get('roll_no') or f"ID-{s['student_id']}",
                    "Student Name": s['name'],
                    "Present": 0,
                    "Total": 0,
                    "Attendance %": "0.0%"
                }
                for s in sorted_roster
            ])
            st.dataframe(empty_df, use_container_width=True, hide_index=True)
        else:
            # Group timestamps into ordered lecture slots
            raw_slots = sorted({
                str(r.get('timestamp')).split(".")[0]
                for r in filtered_records if r.get('timestamp')
            })
            # Check if multiple sessions share the same calendar date
            date_counts = {}
            for slot in raw_slots:
                dt = _parse_iso_dt(slot)
                d_label = dt.strftime("%d %b") if dt else slot
                date_counts[d_label] = date_counts.get(d_label, 0) + 1

            slot_labels = {}
            for slot in raw_slots:
                dt = _parse_iso_dt(slot)
                if dt:
                    d_label = dt.strftime("%d %b")
                    slot_labels[slot] = dt.strftime("%d %b (%H:%M)") if date_counts[d_label] > 1 else d_label
                else:
                    slot_labels[slot] = slot

            # Map (student_id, slot) -> is_present
            att_lookup = {}
            for r in filtered_records:
                slot = str(r.get('timestamp')).split(".")[0] if r.get('timestamp') else None
                if slot:
                    att_lookup[(r['student_id'], slot)] = bool(r.get('is_present', False))

            register_rows = []
            total_present_all = 0
            total_logged_all = 0
            for stu in sorted_roster:
                sid = stu['student_id']
                row = {
                    "Roll No": stu.get('roll_no') or f"ID-{sid}",
                    "Student Name": stu['name'],
                }
                p_cnt = 0
                t_cnt = 0
                for slot in raw_slots:
                    col_lbl = slot_labels[slot]
                    if (sid, slot) in att_lookup:
                        t_cnt += 1
                        if att_lookup[(sid, slot)]:
                            p_cnt += 1
                            row[col_lbl] = "✔ P"
                        else:
                            row[col_lbl] = "✘ A"
                    else:
                        row[col_lbl] = "—"
                pct = round((p_cnt / t_cnt) * 100, 1) if t_cnt > 0 else 0.0
                row["Present"] = p_cnt
                row["Total"] = t_cnt
                row["%"] = f"{pct:.1f}%"
                row["Standing"] = "✅ Safe" if (t_cnt == 0 or pct >= 75.0) else "⚠️ Low"
                register_rows.append(row)
                total_present_all += p_cnt
                total_logged_all += t_cnt

            reg_df = pd.DataFrame(register_rows)

            k1, k2, k3 = st.columns(3)
            avg_pct = round((total_present_all / total_logged_all) * 100, 1) if total_logged_all > 0 else 0.0
            with k1:
                st.metric("👥 Enrolled Students", len(sorted_roster))
            with k2:
                st.metric("📅 Total Lecture Dates", len(raw_slots))
            with k3:
                st.metric("📈 Class Avg Attendance", f"{avg_pct:.1f}%")

            st.dataframe(reg_df, use_container_width=True, hide_index=True)

            csv_bytes = reg_df.to_csv(index=False).encode("utf-8-sig")
            fname_code = selected_sub['subject_code'] if selected_sub else "All"
            st.download_button(
                label="📥 Download Date-Wise Register (Excel CSV)",
                data=csv_bytes,
                file_name=f"Attendance_Register_{fname_code}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

    with tab_sess:
        if not filtered_records:
            st.info("No attendance logs found for this filter.")
        else:
            data = []
            for r in filtered_records:
                ts = r.get('timestamp')
                dt = _parse_iso_dt(ts)
                data.append({
                    "ts_group": str(ts).split(".")[0] if ts else "N/A",
                    "Time": dt.strftime("%Y-%m-%d %I:%M %p") if dt else "N/A",
                    "Roll No": r.get('roll_no') or f"ID-{r.get('student_id')}",
                    "Student Name": r.get('student_name') or f"Student #{r.get('student_id')}",
                    "Subject": r['subjects']['name'],
                    "Subject Code": r['subjects']['subject_code'],
                    "Section": r['subjects'].get('section', '-'),
                    "is_present": bool(r.get('is_present', False)),
                    "Mark": "✔ Present" if r.get('is_present') else "✘ Absent",
                    "Verification": r.get('verification_status', 'Present' if r.get('is_present') else 'Absent'),
                    "_sort": roll_sort_key({'roll_no': r.get('roll_no'), 'name': r.get('student_name'), 'student_id': r.get('student_id')})
                })

            df = pd.DataFrame(data)
            summary = (
                df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code', 'Section'])
                .agg(
                    Present_Count=('is_present', 'sum'),
                    Total_Count=('is_present', 'count')
                ).reset_index()
            )
            summary['Attendance Stats'] = (
                "✅ " + summary['Present_Count'].astype(str) + " / "
                + summary['Total_Count'].astype(str) + ' Students'
            )
            display_df = (
                summary.sort_values(by='ts_group', ascending=False)
                [['Time', 'Subject', 'Subject Code', 'Section', 'Attendance Stats']]
            )
            st.dataframe(display_df, use_container_width=True, hide_index=True)

            with st.expander("🔎 View Individual Student Logs (Roll No. Sorted)"):
                detail_df = df.sort_values(by=['ts_group', '_sort'], ascending=[False, True])[
                    ['Time', 'Roll No', 'Student Name', 'Mark', 'Verification']
                ]
                st.dataframe(detail_df, use_container_width=True, hide_index=True)


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def teacher_screen_login():
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
                Faculty Portal
            </h2>
            <p style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">
                Enter your teacher username and password to continue.
            </p>
        </div>
    """, unsafe_allow_html=True)

    teacher_username = st.text_input("Enter username", placeholder='prof_roy', value='prof_roy')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password", value='admin123')

    st.markdown("""
        <div style="background: #f0fdf4; border: 1px solid #86efac; border-radius: 10px; padding: 10px 14px; margin-bottom: 15px; font-size: 0.9rem; color: #166534;">
            💡 <b>Pre-configured Demo Account:</b> Username: <code>prof_roy</code> &nbsp;|&nbsp; Password: <code>admin123</code>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('🔑 Login', use_container_width=True, type='primary'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid username and password combination")

    with btnc2:
        if st.button('➕ Register Instead', use_container_width=True):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken!"
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match!"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully registered! You can login now."
    except Exception as e:
        return False, f"Registration error: {e}"


def teacher_screen_register():
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("⬅️ Home", type='secondary', key='regbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("""
        <div style="text-align: center; margin: 15px 0 20px 0;">
            <h2 style="color: #0f172a; margin: 0; font-size: 1.8rem; font-weight: 700; font-family: 'Outfit', sans-serif;">
                Register Faculty Profile
            </h2>
        </div>
    """, unsafe_allow_html=True)

    teacher_username = st.text_input("Enter username", placeholder='prof_roy')
    teacher_name = st.text_input("Enter Full Name", placeholder='Prof. Ananya Roy')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")
    teacher_pass_confirm = st.text_input("Confirm password", type='password', placeholder="Enter password")

    st.divider()
    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('📝 Register Now', use_container_width=True, type='primary'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(1)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button('🔑 Login Instead', use_container_width=True):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()
