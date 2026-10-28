import streamlit as st

from src.screens.UI.base_layout import style_background_dashboard, style_base_layout

from pipelines.database.components.header import header_dashboard
from pipelines.database.components.footer import footer_dashboard
from pipelines.database.components.subject_card import subject_card
from pipelines.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher, get_enrolled_students
from pipelines.database.components.dialog_create_subject import create_subject_dialog
from pipelines.database.components.dialog_share_subject import share_subject_dialog
from pipelines.database.components.dialog_add_photo import add_photos_dialog

from pipelines.face_pipeline import predict_attendance, get_threshold_label, DEFAULT_FACE_THRESHOLD
from pipelines.database.components.dialog_attendance_results import attendance_result_dialog, show_attendance_result
from pipelines.reports import generate_college_monthly_excel, build_monthly_matrix_data
import numpy as np

from datetime import datetime

import pandas as pd

from pipelines.database.components.dialog_voice_attendance import voice_attendance_dialog
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()





def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data['teacher_id']

    c1, c2 = st.columns([3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.markdown(f"""
            <div style="text-align:right; margin-bottom:6px;">
                <span style="font-size:1.05rem; font-weight:700; color:#0F172A;">Prof. {teacher_data['name']}</span>
                <span style="background:#EEF2FF; color:#4F46E5; border:1px solid #C7D2FE; font-size:0.75rem; font-weight:700; padding:2px 8px; border-radius:6px; margin-left:6px;">FACULTY</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data 
            st.rerun()

    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # 1. Fetch data and calculate dashboard statistics
    with st.spinner("Calculating stats.."):
        subjects = get_teacher_subjects(teacher_id)
        records = get_attendance_for_teacher(teacher_id)

    total_subjects = len(subjects)
    total_enrollments = sum(sub.get('total_students', 0) for sub in subjects)
    total_sessions = sum(sub.get('total_classes', 0) for sub in subjects)

    total_logs = len(records)
    total_present = sum(1 for r in records if r.get('is_present'))
    overall_rate = (total_present / total_logs * 100) if total_logs > 0 else 100.0

    # Render Stats Cards
    st.markdown("### Dashboard Summary")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.metric(label="Total Subjects", value=total_subjects)
    with t2:
        st.metric(label="Total Enrolled Students", value=total_enrollments)
    with t3:
        st.metric(label="Sessions Conducted", value=total_sessions)
    with t4:
        st.metric(label="Overall Attendance", value=f"{overall_rate:.1f}%")

    st.divider()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, use_container_width=True, icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, use_container_width=True, icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, use_container_width=True, icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    

    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, use_container_width=True, caption=f'Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)

    # Face Recognition Accuracy Tuning Expander
    with st.expander("⚙️ Face Recognition Accuracy Tuning (Nearest-Neighbor Cutoff)", expanded=False):
        st.markdown(
            "Tune how strictly the AI matches student face embeddings. Lower distance threshold enforces **strict precision** (zero false matches); higher threshold increases **recall** for angled faces or low-light classrooms."
        )
        col_pr1, col_pr2, col_pr3 = st.columns(3)
        with col_pr1:
            if st.button("🔒 Strict Preset (0.45)", use_container_width=True, help="High certainty matches only"):
                st.session_state.face_match_threshold = 0.45
                st.rerun()
        with col_pr2:
            if st.button("🎯 Recommended Preset (0.52)", use_container_width=True, help="Optimal balance for classrooms"):
                st.session_state.face_match_threshold = 0.52
                st.rerun()
        with col_pr3:
            if st.button("📸 Lenient Preset (0.60)", use_container_width=True, help="Tolerates angles & distant faces"):
                st.session_state.face_match_threshold = 0.60
                st.rerun()

        current_thresh = float(st.session_state.get('face_match_threshold', DEFAULT_FACE_THRESHOLD))
        chosen_threshold = st.slider(
            "Nearest-Neighbor Distance Cutoff",
            min_value=0.35,
            max_value=0.75,
            value=current_thresh,
            step=0.01,
            key="slider_face_threshold"
        )
        st.session_state.face_match_threshold = chosen_threshold
        st.caption(f"Current Tuning: **{get_threshold_label(chosen_threshold)}** (Distance cutoff: `{chosen_threshold:.2f}`)")

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', use_container_width=True, type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.session_state.face_attendance_review = None
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', use_container_width=True, type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos with nearest-neighbor AI...'):
                all_detected_ids = {}
                threshold_val = float(st.session_state.get('face_match_threshold', DEFAULT_FACE_THRESHOLD))

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np, threshold=threshold_val)

                    if detected:
                        for sid, match_info in detected.items():
                            student_id = int(sid)
                            conf = match_info.get('confidence', 75.0) if isinstance(match_info, dict) else 75.0
                            dist = match_info.get('distance', threshold_val) if isinstance(match_info, dict) else threshold_val
                            all_detected_ids.setdefault(student_id, []).append({
                                "photo": f"Photo {idx+1}",
                                "conf": conf,
                                "dist": dist
                            })

                enrolled_students = get_enrolled_students(selected_subject_id)

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']
                        sid = int(student['student_id'])
                        matches = all_detected_ids.get(sid, [])
                        is_present = len(matches) > 0

                        if is_present:
                            best_match = min(matches, key=lambda m: m['dist'])
                            photos_str = ", ".join([m['photo'] for m in matches])
                            detection_info = f"Detected in {photos_str}"
                            match_score = f"{best_match['conf']:.0f}% (dist: {best_match['dist']:.2f})"
                        else:
                            detection_info = "Not detected by AI camera"
                            match_score = "-"

                        results.append({
                            "Present": bool(is_present),
                            "Roll No": student.get('roll_number') or '-',
                            "Name": student['name'],
                            "Detection Info": detection_info,
                            "Match Score": match_score,
                            "student_id": sid
                        })

                        attendance_to_log.append({
                            'student_id': sid,
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    # Save scan results to session state for persistent interactive review
                    st.session_state.face_attendance_review = (pd.DataFrame(results), attendance_to_log)
                    if "review_df_face" in st.session_state:
                        del st.session_state["review_df_face"]
                    st.rerun()

    with c3:
        if st.button('Use Voice Attendance', type='primary', use_container_width=True, icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)

    # Render Attendance Review & Manual Override Section
    if st.session_state.get('face_attendance_review'):
        st.divider()
        df_review, logs_review = st.session_state.face_attendance_review
        show_attendance_result(df_review, logs_review, key_suffix="face")











def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects')

    with col2:
        if st.button('Create New Subject', use_container_width=True):
            create_subject_dialog(teacher_id)


    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(subject=sub):
                if st.button(f"Share Code: {subject['name']}", key=f"share_{subject['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(subject['name'], subject['subject_code'])
                st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header('Attendance Records & Reports')

    teacher_id = st.session_state.teacher_data['teacher_id']
    subjects = get_teacher_subjects(teacher_id)
    records = get_attendance_for_teacher(teacher_id)

    tab_college, tab_sessions, tab_logs = st.tabs([
        "📊 College Format Consolidated Monthly Report (Roll No Wise)",
        "📋 Session Summaries",
        "🔍 Detailed Student Logs"
    ])

    # =========================================================================
    # TAB 1: College Format Consolidated Monthly Report (Roll No Wise)
    # =========================================================================
    with tab_college:
        st.markdown("### 🎓 College Format Consolidated Attendance Sheet")
        st.markdown(
            "Download and preview academic monthly attendance registers in **standard university format** with Roll No sorting, daily Present (P) / Absent (A) columns, attendance percentages, defaulter flags (<75%), and faculty signatures."
        )

        if not subjects:
            st.info("No subjects found. Please create a subject first in 'Manage Subjects'.")
        else:
            sub_options = {f"{s['name']} ({s['subject_code']}) - Section {s['section']}": s['subject_id'] for s in subjects}
            col_s1, col_s2 = st.columns([2, 1.5])

            with col_s1:
                selected_sub_label = st.selectbox(
                    "Select Subject",
                    options=list(sub_options.keys()),
                    key="college_report_sub"
                )
                chosen_sub_id = sub_options[selected_sub_label]

            # Detect months with attendance data for this subject
            initial_data = build_monthly_matrix_data(chosen_sub_id)
            avail_months = initial_data['stats'].get('available_months', [])

            now = datetime.now()
            current_month_tuple = (now.year, now.month)
            if current_month_tuple not in avail_months:
                avail_months.append(current_month_tuple)
            avail_months.sort(reverse=True)

            month_choices = [("all", "Consolidated (All Recorded Classes)")]
            for yr, mo in avail_months:
                try:
                    lbl = datetime(yr, mo, 1).strftime("%B %Y")
                except Exception:
                    lbl = f"Month {mo}/{yr}"
                month_choices.append(((yr, mo), lbl))

            month_labels = [m[1] for m in month_choices]

            with col_s2:
                selected_month_label = st.selectbox(
                    "Select Academic Month & Year",
                    options=month_labels,
                    index=0,
                    key="college_report_month"
                )

            # Determine selected month/year filter
            selected_choice = next(m for m in month_choices if m[1] == selected_month_label)
            if selected_choice[0] == "all":
                filter_yr, filter_mo = None, None
                month_slug = "Consolidated_All"
            else:
                filter_yr, filter_mo = selected_choice[0]
                month_slug = f"{filter_yr}_{filter_mo:02d}"

            # Build full matrix data
            matrix_result = build_monthly_matrix_data(chosen_sub_id, month=filter_mo, year=filter_yr)
            sub_info = matrix_result['subject']
            matrix_df = matrix_result['df']
            stats = matrix_result['stats']

            st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

            # Metrics Banner
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Total Students Enrolled", stats['total_students'])
            with m2:
                st.metric("Classes Held in Period", stats['total_classes'])
            with m3:
                st.metric("Average Class Attendance", f"{stats['average_attendance']}%")
            with m4:
                def_cnt = stats['defaulters_count']
                st.metric(
                    "Defaulters (<75% Attendance)",
                    f"{def_cnt} Students",
                    delta=f"-{def_cnt}" if def_cnt > 0 else "0",
                    delta_color="inverse"
                )

            st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

            # Download Buttons
            dl_col1, dl_col2 = st.columns(2)
            safe_code = str(sub_info.get('subject_code', 'Report')).replace(' ', '_')

            with dl_col1:
                try:
                    excel_bytes = generate_college_monthly_excel(chosen_sub_id, month=filter_mo, year=filter_yr)
                    st.download_button(
                        label="📊 Download College Format Consolidated Excel (.xlsx)",
                        data=excel_bytes,
                        file_name=f"College_Attendance_{safe_code}_{month_slug}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        type="primary",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error preparing Excel report: {e}")

            with dl_col2:
                csv_matrix_bytes = matrix_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Export Consolidated Matrix to CSV",
                    data=csv_matrix_bytes,
                    file_name=f"Attendance_Matrix_{safe_code}_{month_slug}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

            # Interactive On-Screen Table Preview
            st.markdown("#### 📋 On-Screen Consolidated Matrix (Roll No Wise)")

            search_mat = st.text_input(
                "Filter Matrix by Roll No or Student Name",
                placeholder="Type to filter rows...",
                key="filter_matrix_search"
            )

            preview_df = matrix_df.copy()
            if search_mat.strip() and not preview_df.empty:
                q = search_mat.strip().lower()
                preview_df = preview_df[
                    preview_df['Roll No'].astype(str).str.lower().str.contains(q) |
                    preview_df['Student Name'].astype(str).str.lower().str.contains(q)
                ]

            if preview_df.empty:
                st.info("No attendance records found matching the criteria.")
            else:
                st.dataframe(
                    preview_df,
                    use_container_width=True,
                    hide_index=True
                )
                if stats['defaulters_count'] > 0:
                    st.warning(f"⚠️ Note: {stats['defaulters_count']} student(s) fall below the college minimum 75% attendance threshold.")

    # =========================================================================
    # TAB 2: Class Session Summaries
    # =========================================================================
    with tab_sessions:
        if not records:
            st.info("No attendance records found yet.")
        else:
            data = []
            for r in records:
                ts = r.get('timestamp')
                dt = None
                if ts:
                    try:
                        dt = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
                    except Exception:
                        dt = None

                subj = r.get('subjects') or {}
                stud = r.get('students') or {}

                data.append({
                    "timestamp": ts,
                    "date": dt.date() if dt else None,
                    "Time": dt.strftime("%Y-%m-%d %I:%M %p") if dt else (str(ts) if ts else "N/A"),
                    "Subject": subj.get('name', 'Unknown Subject'),
                    "Subject Code": subj.get('subject_code', '-'),
                    "Roll No": stud.get('roll_number') or '-',
                    "Student Name": stud.get('name', 'Unknown Student'),
                    "is_present": bool(r.get('is_present', False)),
                    "Status": "✅ Present" if r.get('is_present') else "❌ Absent"
                })

            df_records = pd.DataFrame(data)

            st.markdown("#### Search & Filter Sessions")
            c_s1, c_s2 = st.columns([2, 2])
            with c_s1:
                search_q = st.text_input("Search Sessions by Subject Name or Code", placeholder="E.g. Computer Networking, 401", key="search_sess")
            with c_s2:
                min_date = df_records['date'].min()
                max_date = df_records['date'].max()
                if min_date and max_date and min_date != max_date:
                    date_range = st.date_input("Filter Sessions by Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="date_sess")
                else:
                    date_range = st.date_input("Filter Sessions by Date Range", key="date_sess")

            df_filt_sess = df_records.copy()
            if search_q.strip():
                sq = search_q.strip().lower()
                df_filt_sess = df_filt_sess[
                    df_filt_sess['Subject'].str.lower().str.contains(sq) |
                    df_filt_sess['Subject Code'].str.lower().str.contains(sq)
                ]
            if isinstance(date_range, tuple) and len(date_range) == 2:
                s_date, e_date = date_range
                df_filt_sess = df_filt_sess[(df_filt_sess['date'] >= s_date) & (df_filt_sess['date'] <= e_date)]
            elif isinstance(date_range, datetime) or isinstance(date_range, pd.Timestamp):
                df_filt_sess = df_filt_sess[df_filt_sess['date'] == date_range]

            if df_filt_sess.empty:
                st.warning("No session records matched the filter.")
            else:
                summary = (
                    df_filt_sess.groupby(['timestamp', 'Time', 'Subject', 'Subject Code'])
                    .agg(
                        Present_Count = ('is_present', 'sum'),
                        Total_Count = ('is_present', 'count')
                    ).reset_index()
                )
                summary['Attendance Stats'] = (
                    "✅ " + summary['Present_Count'].astype(str) + " / "
                    + summary['Total_Count'].astype(str) + ' Students'
                )
                summary['Attendance Rate'] = (
                    (summary['Present_Count'] / summary['Total_Count'] * 100).round(1).astype(str) + "%"
                )
                display_sess = summary.sort_values(by='timestamp', ascending=False)[
                    ['Time', 'Subject', 'Subject Code', 'Attendance Stats', 'Attendance Rate']
                ]
                st.dataframe(display_sess, use_container_width=True, hide_index=True)

                csv_sess = display_sess.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Session Summaries to CSV",
                    data=csv_sess,
                    file_name=f"session_summaries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    # =========================================================================
    # TAB 3: Detailed Student Logs
    # =========================================================================
    with tab_logs:
        if not records:
            st.info("No detailed logs available.")
        else:
            st.markdown("#### Search Individual Student Logs")
            c_l1, c_l2 = st.columns([2, 1])
            with c_l1:
                search_stud = st.text_input("Search by Roll No, Student Name, or Subject", placeholder="E.g. 21CS042, Pratyush", key="search_stud_log")
            with c_l2:
                status_filter = st.selectbox("Status Filter", options=["All", "✅ Present Only", "❌ Absent Only"], key="filter_status_log")

            df_filt_logs = df_records.copy()
            if search_stud.strip():
                sql = search_stud.strip().lower()
                df_filt_logs = df_filt_logs[
                    df_filt_logs['Subject'].str.lower().str.contains(sql) |
                    df_filt_logs['Subject Code'].str.lower().str.contains(sql) |
                    df_filt_logs['Roll No'].astype(str).str.lower().str.contains(sql) |
                    df_filt_logs['Student Name'].str.lower().str.contains(sql)
                ]

            if status_filter == "✅ Present Only":
                df_filt_logs = df_filt_logs[df_filt_logs['is_present'] == True]
            elif status_filter == "❌ Absent Only":
                df_filt_logs = df_filt_logs[df_filt_logs['is_present'] == False]

            if df_filt_logs.empty:
                st.warning("No individual logs matched the filter.")
            else:
                display_logs = df_filt_logs.sort_values(by='timestamp', ascending=False)[
                    ['Time', 'Subject', 'Subject Code', 'Roll No', 'Student Name', 'Status']
                ]
                st.dataframe(display_logs, use_container_width=True, hide_index=True)

                csv_logs = display_logs.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Export Detailed Student Logs to CSV",
                    data=csv_logs,
                    file_name=f"student_attendance_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )


def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    

    return False
def teacher_screen_login():
    c1, c2 = st.columns([3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    pad1, center_col, pad2 = st.columns([1, 1.8, 1])
    with center_col:
        st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:2rem 2.2rem; box-shadow:0 10px 30px -5px rgba(0,0,0,0.05); margin-bottom:1.5rem;">
                <h3 style="margin:0 0 6px 0; color:#0F172A; text-align:center;">Faculty Login</h3>
                <p style="color:#64748B; font-size:0.9rem; text-align:center; margin-bottom:1.5rem;">Enter your faculty credentials to access the teacher dashboard</p>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='E.g. vinaypandey', key="teacher_login_user")
        teacher_pass = st.text_input("Password", type='password', placeholder="Enter your password", key="teacher_login_pwd")

        st.markdown("</div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)
        with btnc1:
            if st.button('Login →', type='primary', icon=':material/login:', shortcut='control+enter', use_container_width=True):
                if login_teacher(teacher_username, teacher_pass):
                    st.success("Welcome back! 👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with btnc2:
            if st.button('Register Instead', type="secondary", icon=':material/person_add:', use_container_width=True):
                st.session_state.teacher_login_type = 'register'
                st.rerun()

    footer_dashboard()



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"
    

def teacher_screen_register():
    c1, c2 = st.columns([3, 1.2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("← Back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace", use_container_width=True):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    pad1, center_col, pad2 = st.columns([1, 1.8, 1])
    with center_col:
        st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:20px; padding:2rem 2.2rem; box-shadow:0 10px 30px -5px rgba(0,0,0,0.05); margin-bottom:1.5rem;">
                <h3 style="margin:0 0 6px 0; color:#0F172A; text-align:center;">Register Faculty Profile</h3>
                <p style="color:#64748B; font-size:0.9rem; text-align:center; margin-bottom:1.5rem;">Create an instructor account to manage classes and attendance</p>
        """, unsafe_allow_html=True)
        
        teacher_username = st.text_input("Choose Username *", placeholder='E.g. vinaypandey')
        teacher_name = st.text_input("Full Name *", placeholder='E.g. Prof. Vinay Pandey')
        teacher_pass = st.text_input("Password *", type='password', placeholder="Enter secure password")
        teacher_pass_confirm = st.text_input("Confirm Password *", type='password', placeholder="Re-enter password")

        st.markdown("</div>", unsafe_allow_html=True)

        btnc1, btnc2 = st.columns(2)
        with btnc1:
            if st.button('Register now', type='primary', icon=':material/check:', shortcut='control+enter', use_container_width=True):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    import time
                    time.sleep(1.5)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button('Login Instead', type="secondary", icon=':material/login:', use_container_width=True):
                st.session_state.teacher_login_type = 'login'
                st.rerun()

    footer_dashboard()