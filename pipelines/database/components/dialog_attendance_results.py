import streamlit as st
from pipelines.database.db import create_attendance
import time
import pandas as pd

def show_attendance_result(df, logs, key_suffix="default"):
    """
    Renders the interactive Attendance Review & Manual Override component.
    Allows teachers to review AI detections, toggle individual student Present/Absent checkboxes,
    use quick batch actions (Mark All Present/Absent/Reset), and safely commit to the database.
    """
    st.markdown("### 📋 Attendance Review & Manual Override")
    st.info("💡 **Teacher Override**: Toggle any student's checkbox below to mark them **Present (Checked ✅)** or **Absent (Unchecked ❌)** if the camera or voice scan missed them.")

    if df is None or len(df) == 0:
        st.warning("No student records available to review.")
        return

    # Ensure Present column exists
    df_working = df.copy()
    if "Present" not in df_working.columns:
        if "Status" in df_working.columns:
            df_working["Present"] = df_working["Status"].astype(str).str.contains("Present")
        else:
            df_working["Present"] = False

    # Store AI detected baseline if not present (for reset button)
    if "AI_Baseline" not in df_working.columns:
        df_working["AI_Baseline"] = df_working["Present"].copy()

    # Session key for tracking current review dataframe
    state_key = f"review_df_{key_suffix}"
    if state_key not in st.session_state:
        st.session_state[state_key] = df_working.copy()

    current_df = st.session_state[state_key]

    # Quick Batch Actions
    btn_c1, btn_c2, btn_c3, _ = st.columns([1.2, 1.2, 1.4, 2])
    with btn_c1:
        if st.button("✅ Mark All Present", key=f"btn_all_p_{key_suffix}", use_container_width=True):
            current_df["Present"] = True
            st.session_state[state_key] = current_df
            st.rerun()

    with btn_c2:
        if st.button("❌ Mark All Absent", key=f"btn_all_a_{key_suffix}", use_container_width=True):
            current_df["Present"] = False
            st.session_state[state_key] = current_df
            st.rerun()

    with btn_c3:
        if st.button("🔄 Reset to AI Scan", key=f"btn_reset_{key_suffix}", use_container_width=True):
            if "AI_Baseline" in current_df.columns:
                current_df["Present"] = current_df["AI_Baseline"].copy()
            st.session_state[state_key] = current_df
            st.rerun()

    # Live summary counters
    present_cnt = int(current_df["Present"].sum())
    total_cnt = len(current_df)
    absent_cnt = total_cnt - present_cnt
    attendance_rate = (present_cnt / total_cnt * 100.0) if total_cnt > 0 else 0.0

    st.markdown(
        f"""
        <div style='display:flex; flex-wrap:wrap; gap:12px; margin: 16px 0; background:#FFFFFF; padding:12px 18px; border-radius:16px; border:1px solid #E2E8F0; font-size:0.9rem; box-shadow: 0 4px 16px -2px rgba(0,0,0,0.04); align-items:center;'>
            <span style='background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; padding:4px 12px; border-radius:999px; font-weight:700;'>✅ Present: {present_cnt}</span>
            <span style='background:#FEF2F2; color:#DC2626; border:1px solid #FECACA; padding:4px 12px; border-radius:999px; font-weight:700;'>❌ Absent: {absent_cnt}</span>
            <span style='background:#EEF2FF; color:#4F46E5; border:1px solid #C7D2FE; padding:4px 12px; border-radius:999px; font-weight:700;'>📊 Rate: {attendance_rate:.1f}%</span>
            <span style='background:#F8FAFC; color:#475569; border:1px solid #E2E8F0; padding:4px 12px; border-radius:999px; font-weight:600; margin-left:auto;'>👥 Total Enrolled: {total_cnt}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Search filter within review list
    search_q = st.text_input(
        "🔍 Search by Student Name or Roll Number",
        placeholder="Filter student list...",
        key=f"search_filter_{key_suffix}"
    )

    # Prepare display columns
    display_cols = ["Present", "Roll No", "Name", "Detection Info"]
    if "Match Score" in current_df.columns:
        display_cols.append("Match Score")

    # Keep student_id in the dataframe for robust mapping
    extra_cols = [c for c in ["student_id", "AI_Baseline"] if c in current_df.columns]
    full_cols = [c for c in display_cols if c in current_df.columns] + extra_cols

    filtered_display_df = current_df[full_cols].copy()
    if search_q.strip():
        sq = search_q.strip().lower()
        mask = (
            filtered_display_df["Name"].astype(str).str.lower().str.contains(sq) |
            filtered_display_df["Roll No"].astype(str).str.lower().str.contains(sq)
        )
        filtered_display_df = filtered_display_df[mask]

    # Column configuration
    col_cfg = {
        "Present": st.column_config.CheckboxColumn(
            "Present?",
            help="Check to mark Present (✅), uncheck to mark Absent (❌)",
            default=False
        ),
        "Roll No": st.column_config.TextColumn("Roll No", width="small", disabled=True),
        "Name": st.column_config.TextColumn("Student Name", width="medium", disabled=True),
        "Detection Info": st.column_config.TextColumn("AI Detection Status", width="large", disabled=True),
    }
    if "Match Score" in filtered_display_df.columns:
        col_cfg["Match Score"] = st.column_config.TextColumn("AI Confidence / Dist", width="medium", disabled=True)
    if "student_id" in filtered_display_df.columns:
        col_cfg["student_id"] = None  # Hide internal student_id
    if "AI_Baseline" in filtered_display_df.columns:
        col_cfg["AI_Baseline"] = None  # Hide internal baseline

    # Interactive data editor for checkboxes
    disabled_columns = [c for c in filtered_display_df.columns if c != "Present"]

    edited_view = st.data_editor(
        filtered_display_df,
        column_config=col_cfg,
        disabled=disabled_columns,
        hide_index=True,
        use_container_width=True,
        key=f"editor_{key_suffix}"
    )

    # Sync any edits back to current_df
    if "student_id" in edited_view.columns:
        for _, row in edited_view.iterrows():
            sid = row["student_id"]
            current_df.loc[current_df["student_id"] == sid, "Present"] = bool(row["Present"])
        st.session_state[state_key] = current_df

    st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    # Action Confirmation Buttons
    col_act1, col_act2 = st.columns(2)

    with col_act1:
        if st.button("❌ Discard & Cancel", key=f"btn_discard_{key_suffix}", use_container_width=True, type="secondary"):
            st.session_state[state_key] = None
            st.session_state.face_attendance_review = None
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col_act2:
        if st.button("💾 Confirm & Save Attendance", key=f"btn_save_{key_suffix}", use_container_width=True, type="primary"):
            try:
                # Map student_id -> overridden is_present status
                status_map = {}
                for _, r in current_df.iterrows():
                    sid = r.get("student_id")
                    if sid is not None:
                        status_map[int(sid)] = bool(r["Present"])

                updated_logs = []
                for item in logs:
                    sid = item.get("student_id")
                    if sid in status_map:
                        item_copy = dict(item)
                        item_copy["is_present"] = status_map[sid]
                        updated_logs.append(item_copy)
                    else:
                        updated_logs.append(dict(item))

                # Save final overridden logs to database
                create_attendance(updated_logs)
                final_present = sum(1 for l in updated_logs if l.get("is_present"))
                final_absent = len(updated_logs) - final_present

                st.success(f"🎉 Attendance successfully saved! ({final_present} Present ✅, {final_absent} Absent ❌)")
                st.session_state[state_key] = None
                st.session_state.face_attendance_review = None
                st.session_state.voice_attendance_results = None
                st.session_state.attendance_images = []
                time.sleep(1.2)
                st.rerun()
            except Exception as e:
                print(f"[Save Attendance Error]: {e}")
                st.error(f"Save failed: {e}")

@st.dialog("Attendance Review & Manual Override")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs, key_suffix="dialog")
