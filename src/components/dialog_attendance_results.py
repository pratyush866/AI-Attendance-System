import streamlit as st
from src.database.db import create_attendance, close_attendance_session


def show_attendance_result(df, logs, session_id=None):
    st.write(
        "Review AI verification results below. You can tick/untick the **Present (✔)** checkbox "
        "to manually correct any student before saving to the register:"
    )

    if "Present" in df.columns:
        disabled_cols = [c for c in df.columns if c != "Present"]
        edited_df = st.data_editor(
            df,
            hide_index=True,
            use_container_width=True,
            disabled=disabled_cols,
            column_config={
                "Present": st.column_config.CheckboxColumn("Present (✔)", default=False)
            },
            key=f"att_editor_{session_id or 'manual'}"
        )
        present_count = int(edited_df["Present"].sum())
    else:
        st.dataframe(df, hide_index=True, use_container_width=True)
        edited_df = df
        present_count = sum(1 for lg in logs if lg.get("is_present"))

    st.caption(f"📊 Ready to Save: **{present_count} / {len(logs)} Students Marked Present**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard', use_container_width=True):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('Confirm & Save Final Attendance', use_container_width=True, type='primary'):
            try:
                final_logs = []
                for idx, log in enumerate(logs):
                    updated = dict(log)
                    if "Present" in edited_df.columns and idx < len(edited_df):
                        new_present = bool(edited_df.iloc[idx]["Present"])
                        if new_present != bool(log.get("is_present")):
                            updated["is_present"] = new_present
                            updated["verification_status"] = (
                                "🟢 Present (Teacher Verified)" if new_present else "❌ Absent (Teacher Updated)"
                            )
                    final_logs.append(updated)

                create_attendance(final_logs)
                if session_id:
                    close_attendance_session(session_id)
                    for k in list(st.session_state.keys()):
                        if k.startswith("active_session_"):
                            sess = st.session_state.get(k)
                            if isinstance(sess, dict) and sess.get("session_id") == session_id:
                                del st.session_state[k]
                st.success("✅ Attendance successfully saved to register!")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f'Sync failed: {e}')


@st.dialog("📋 Final Attendance Verification Report")
def attendance_result_dialog(df, logs, session_id=None):
    show_attendance_result(df, logs, session_id=session_id)
