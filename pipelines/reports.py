import io
import re
from datetime import datetime
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from pipelines.database.db import (
    get_enrolled_students,
    get_attendance_for_subject,
    get_subject_by_id
)

def natural_roll_key(roll):
    """Sort key for natural ordering of roll numbers (e.g. 1, 2, 10 instead of 1, 10, 2)."""
    if not roll or str(roll).strip() in ('-', '', 'None'):
        return (1, [999999])
    roll_str = str(roll).strip()
    parts = [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', roll_str)]
    return (0, parts)

def parse_iso_datetime(ts_str):
    """Safely parse ISO or standard timestamp string into datetime."""
    if not ts_str:
        return None
    try:
        clean = str(ts_str).replace('Z', '+00:00').strip()
        return datetime.fromisoformat(clean)
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(ts_str).split('.')[0], fmt)
        except Exception:
            continue
    return None

def build_monthly_matrix_data(subject_id: int, month: int = None, year: int = None):
    """
    Builds the consolidated attendance matrix for a given subject and optional month/year.
    
    Returns:
        dict with:
            'subject': subject dict
            'month_label': e.g. 'October 2026' or 'All Recorded Sessions'
            'df': pandas DataFrame ready for display or CSV export
            'sessions': list of dicts with session keys and formatted headers
            'stats': overall summary metrics
    """
    subject = get_subject_by_id(subject_id) or {
        "subject_id": subject_id,
        "name": f"Subject #{subject_id}",
        "subject_code": "-",
        "section": "-",
        "teacher_name": "Faculty"
    }

    # 1. Enrolled Students
    enrolled_nodes = get_enrolled_students(subject_id)
    students = []
    for node in enrolled_nodes:
        s = node.get('students') or {}
        if s and s.get('student_id'):
            students.append({
                'student_id': s['student_id'],
                'roll_number': s.get('roll_number') or '-',
                'name': s.get('name') or 'Unnamed Student'
            })

    # Sort students by Roll Number (natural sort) then by name
    students.sort(key=lambda x: (natural_roll_key(x['roll_number']), x['name'].lower()))

    # 2. Attendance Logs for this subject
    logs = get_attendance_for_subject(subject_id)

    # Filter logs by month and year if requested
    filtered_logs = []
    available_months = set()

    for log in logs:
        ts = log.get('timestamp')
        dt = parse_iso_datetime(ts)
        if dt:
            available_months.add((dt.year, dt.month))
            if month is not None and dt.month != month:
                continue
            if year is not None and dt.year != year:
                continue
            filtered_logs.append((dt, log))
        else:
            if month is None and year is None:
                filtered_logs.append((datetime.min, log))

    # Determine unique session timestamps
    unique_session_timestamps = sorted(list(set(item[1].get('timestamp') for item in filtered_logs if item[1].get('timestamp'))))
    
    # Map session timestamp to human-readable date header
    # Check if multiple sessions on the same date to avoid ambiguous column names
    date_counts = {}
    parsed_sessions = []
    for ts in unique_session_timestamps:
        dt = parse_iso_datetime(ts)
        d_str = dt.strftime("%d-%b") if dt else "Session"
        date_counts[d_str] = date_counts.get(d_str, 0) + 1
        parsed_sessions.append((ts, dt, d_str))

    date_occurrences = {}
    session_cols = []
    for ts, dt, d_str in parsed_sessions:
        if date_counts.get(d_str, 0) > 1:
            date_occurrences[d_str] = date_occurrences.get(d_str, 0) + 1
            col_header = f"{d_str} (S{date_occurrences[d_str]})"
        else:
            col_header = dt.strftime("%d-%b (%a)") if dt else d_str
        session_cols.append({
            'timestamp': ts,
            'datetime': dt,
            'header': col_header
        })

    # Build student attendance lookup: (student_id, timestamp) -> is_present
    attendance_lookup = {}
    for dt, log in filtered_logs:
        sid = log.get('student_id')
        ts = log.get('timestamp')
        is_p = bool(log.get('is_present', False))
        attendance_lookup[(sid, ts)] = is_p

    # Month label
    if month is not None and year is not None:
        try:
            month_label = datetime(year, month, 1).strftime("%B %Y")
        except Exception:
            month_label = f"Month {month}/{year}"
    elif month is not None:
        month_label = f"Month {month}"
    else:
        month_label = "Consolidated (All Recorded Classes)"

    # Build row matrix
    rows = []
    total_classes = len(session_cols)

    for idx, stud in enumerate(students, start=1):
        sid = stud['student_id']
        row = {
            "Sr No": idx,
            "Roll No": stud['roll_number'],
            "Student Name": stud['name'],
        }
        attended_count = 0

        for s_info in session_cols:
            ts = s_info['timestamp']
            header = s_info['header']
            is_p = attendance_lookup.get((sid, ts), False)
            if is_p:
                row[header] = "P"
                attended_count += 1
            else:
                row[header] = "A"

        absent_count = total_classes - attended_count
        pct = (attended_count / total_classes * 100.0) if total_classes > 0 else 100.0
        
        row["Total Held"] = total_classes
        row["Attended"] = attended_count
        row["Absent"] = absent_count
        row["Percentage (%)"] = round(pct, 1)
        row["Eligibility Status"] = "Eligible" if pct >= 75.0 else "Shortage (<75%)"
        
        rows.append(row)

    df_matrix = pd.DataFrame(rows)

    # Class-level summary statistics
    total_students = len(students)
    defaulters_count = sum(1 for r in rows if r["Percentage (%)"] < 75.0) if total_classes > 0 else 0
    avg_pct = (sum(r["Percentage (%)"] for r in rows) / total_students) if total_students > 0 else 100.0

    stats = {
        "total_students": total_students,
        "total_classes": total_classes,
        "average_attendance": round(avg_pct, 1),
        "defaulters_count": defaulters_count,
        "available_months": sorted(list(available_months))
    }

    return {
        "subject": subject,
        "month_label": month_label,
        "df": df_matrix,
        "sessions": session_cols,
        "stats": stats,
        "students": students
    }


def generate_college_monthly_excel(subject_id: int, month: int = None, year: int = None) -> bytes:
    """
    Generates a beautifully styled, college-format consolidated monthly attendance report
    in Microsoft Excel (.xlsx) format using openpyxl.
    """
    matrix_data = build_monthly_matrix_data(subject_id, month=month, year=year)
    subject = matrix_data['subject']
    month_label = matrix_data['month_label']
    df = matrix_data['df']
    sessions = matrix_data['sessions']
    stats = matrix_data['stats']

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Monthly Attendance"

    # Explicitly show grid lines
    ws.views.sheetView[0].showGridLines = True

    # Styling Palettes
    navy_dark = "1E3A8A"
    blue_header = "2563EB"
    meta_bg = "F1F5F9"
    green_p_fill = "DCFCE7"
    green_p_font = "15803D"
    red_a_fill = "FEE2E2"
    red_a_font = "B91C1C"
    warning_fill = "FEF2F2"
    border_gray = "CBD5E1"
    zebra_bg = "F8FAFC"

    font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    font_subtitle = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_meta_label = Font(name="Calibri", size=10, bold=True, color="1E293B")
    font_meta_val = Font(name="Calibri", size=10, bold=False, color="0F172A")
    font_col_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_cell_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
    font_cell_regular = Font(name="Calibri", size=10, bold=False, color="0F172A")
    font_p = Font(name="Calibri", size=10, bold=True, color=green_p_font)
    font_a = Font(name="Calibri", size=10, bold=True, color=red_a_font)
    font_defaulter = Font(name="Calibri", size=10, bold=True, color="DC2626")
    font_eligible = Font(name="Calibri", size=10, bold=True, color="15803D")

    fill_title = PatternFill(start_color=navy_dark, end_color=navy_dark, fill_type="solid")
    fill_col_header = PatternFill(start_color=blue_header, end_color=blue_header, fill_type="solid")
    fill_meta = PatternFill(start_color=meta_bg, end_color=meta_bg, fill_type="solid")
    fill_p = PatternFill(start_color=green_p_fill, end_color=green_p_fill, fill_type="solid")
    fill_a = PatternFill(start_color=red_a_fill, end_color=red_a_fill, fill_type="solid")
    fill_defaulter = PatternFill(start_color=warning_fill, end_color=warning_fill, fill_type="solid")
    fill_zebra = PatternFill(start_color=zebra_bg, end_color=zebra_bg, fill_type="solid")

    thin_side = Side(border_style="thin", color=border_gray)
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    thick_bottom = Border(bottom=Side(border_style="medium", color="0F172A"))

    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    # Determine total columns needed
    # Columns: Sr No (1), Roll No (2), Name (3), Sessions (len), Held, Attended, Absent, Pct, Status
    session_count = len(sessions)
    total_cols = 3 + session_count + 5

    # 1. Institution Title Banner (Row 1 & 2)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=total_cols)
    c1 = ws.cell(row=1, column=1)
    c1.value = "SNAPCLASS ACADEMIC PORTAL - CONSOLIDATED MONTHLY ATTENDANCE REGISTER"
    c1.font = font_title
    c1.fill = fill_title
    c1.alignment = align_center

    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=total_cols)
    c2 = ws.cell(row=2, column=1)
    c2.value = f"COLLEGE ATTENDANCE REPORT | {month_label.upper()} | SUBJECT: {subject.get('name', '').upper()}"
    c2.font = font_subtitle
    c2.fill = fill_title
    c2.alignment = align_center

    # 2. Metadata Section (Rows 3, 4, 5)
    meta_rows = [
        [
            ("Course / Subject:", subject.get('name', 'N/A')),
            ("Subject Code:", subject.get('subject_code', '-')),
            ("Section / Batch:", subject.get('section', '-'))
        ],
        [
            ("Faculty In-Charge:", subject.get('teacher_name') or "Prof. In-Charge"),
            ("Month & Year:", month_label),
            ("Sessions Conducted:", str(stats['total_classes']))
        ],
        [
            ("Total Students:", str(stats['total_students'])),
            ("Class Avg Attendance:", f"{stats['average_attendance']}%"),
            ("Report Generated On:", datetime.now().strftime("%d-%b-%Y %I:%M %p"))
        ]
    ]

    for r_idx, m_items in enumerate(meta_rows, start=3):
        # Background fill across entire meta row
        for c_idx in range(1, total_cols + 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.fill = fill_meta

        # Distribute items across the row
        step = max(1, total_cols // len(m_items))
        for item_idx, (k, v) in enumerate(m_items):
            col_pos = (item_idx * step) + 1
            lbl_cell = ws.cell(row=r_idx, column=col_pos)
            lbl_cell.value = f"{k} {v}"
            lbl_cell.font = font_meta_label
            lbl_cell.alignment = align_left

    # Row 6: Blank spacing
    ws.row_dimensions[6].height = 8

    # 3. Table Column Headers (Row 7)
    headers = ["Sr No", "Roll No", "Student Name"]
    for s in sessions:
        headers.append(s['header'])
    headers.extend(["Total Held", "Attended", "Absent", "Attendance (%)", "Eligibility Status"])

    ws.row_dimensions[7].height = 28
    for col_idx, header_text in enumerate(headers, start=1):
        cell = ws.cell(row=7, column=col_idx)
        cell.value = header_text
        cell.font = font_col_header
        cell.fill = fill_col_header
        cell.alignment = align_center
        cell.border = thin_border

    # 4. Data Rows (starting from Row 8)
    current_row = 8

    if df.empty or len(df) == 0:
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row + 1, end_column=total_cols)
        empty_cell = ws.cell(row=current_row, column=1)
        empty_cell.value = "No attendance records found for this period."
        empty_cell.font = font_cell_bold
        empty_cell.alignment = align_center
        current_row += 2
    else:
        for idx, row in df.iterrows():
            ws.row_dimensions[current_row].height = 20
            is_zebra = (idx % 2 == 1)

            # Col 1: Sr No
            c_sr = ws.cell(row=current_row, column=1, value=int(row["Sr No"]))
            c_sr.font = font_cell_regular
            c_sr.alignment = align_center
            c_sr.border = thin_border
            if is_zebra: c_sr.fill = fill_zebra

            # Col 2: Roll No
            c_roll = ws.cell(row=current_row, column=2, value=str(row["Roll No"]))
            c_roll.font = font_cell_bold
            c_roll.alignment = align_center
            c_roll.border = thin_border
            if is_zebra: c_roll.fill = fill_zebra

            # Col 3: Student Name
            c_name = ws.cell(row=current_row, column=3, value=str(row["Student Name"]))
            c_name.font = font_cell_regular
            c_name.alignment = align_left
            c_name.border = thin_border
            if is_zebra: c_name.fill = fill_zebra

            # Date Columns
            col_ptr = 4
            for s in sessions:
                val = str(row.get(s['header'], 'A'))
                c_date = ws.cell(row=current_row, column=col_ptr, value=val)
                c_date.alignment = align_center
                c_date.border = thin_border

                if val == "P":
                    c_date.font = font_p
                    c_date.fill = fill_p
                else:
                    c_date.font = font_a
                    c_date.fill = fill_a
                col_ptr += 1

            # Summary Columns
            # Total Held
            c_held = ws.cell(row=current_row, column=col_ptr, value=int(row["Total Held"]))
            c_held.font = font_cell_regular
            c_held.alignment = align_center
            c_held.border = thin_border
            if is_zebra: c_held.fill = fill_zebra
            col_ptr += 1

            # Attended
            c_att = ws.cell(row=current_row, column=col_ptr, value=int(row["Attended"]))
            c_att.font = font_cell_bold
            c_att.alignment = align_center
            c_att.border = thin_border
            if is_zebra: c_att.fill = fill_zebra
            col_ptr += 1

            # Absent
            c_abs = ws.cell(row=current_row, column=col_ptr, value=int(row["Absent"]))
            c_abs.font = font_cell_regular
            c_abs.alignment = align_center
            c_abs.border = thin_border
            if is_zebra: c_abs.fill = fill_zebra
            col_ptr += 1

            # Attendance Percentage
            pct_val = float(row["Percentage (%)"])
            c_pct = ws.cell(row=current_row, column=col_ptr, value=f"{pct_val:.1f}%")
            c_pct.alignment = align_center
            c_pct.border = thin_border
            if pct_val < 75.0 and session_count > 0:
                c_pct.font = font_defaulter
                c_pct.fill = fill_defaulter
            else:
                c_pct.font = font_eligible
                if is_zebra: c_pct.fill = fill_zebra
            col_ptr += 1

            # Eligibility Status
            status_val = str(row["Eligibility Status"])
            c_stat = ws.cell(row=current_row, column=col_ptr, value=status_val)
            c_stat.alignment = align_center
            c_stat.border = thin_border
            if status_val.startswith("Shortage"):
                c_stat.font = font_defaulter
                c_stat.fill = fill_defaulter
            else:
                c_stat.font = font_eligible
                if is_zebra: c_stat.fill = fill_zebra

            current_row += 1

    # 5. Class Summary Footer Rows (Total Present per session & Daily Attendance %)
    if not df.empty and session_count > 0:
        # Row A: Total Present on each date
        ws.row_dimensions[current_row].height = 22
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=3)
        lbl_pres = ws.cell(row=current_row, column=1, value="TOTAL STUDENTS PRESENT")
        lbl_pres.font = font_cell_bold
        lbl_pres.alignment = align_right
        lbl_pres.border = thin_border

        for c in range(2, 4):
            ws.cell(row=current_row, column=c).border = thin_border

        for s_idx, s in enumerate(sessions):
            col_idx = 4 + s_idx
            pres_cnt = (df[s['header']] == "P").sum()
            c_sum = ws.cell(row=current_row, column=col_idx, value=int(pres_cnt))
            c_sum.font = font_cell_bold
            c_sum.alignment = align_center
            c_sum.border = thin_border
            c_sum.fill = fill_meta

        # Merge summary trailer columns
        for c in range(4 + session_count, total_cols + 1):
            ws.cell(row=current_row, column=c).border = thin_border
            ws.cell(row=current_row, column=c).fill = fill_meta

        current_row += 1

        # Row B: Daily Attendance Percentage
        ws.row_dimensions[current_row].height = 22
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=3)
        lbl_rate = ws.cell(row=current_row, column=1, value="SESSION ATTENDANCE RATE")
        lbl_rate.font = font_cell_bold
        lbl_rate.alignment = align_right
        lbl_rate.border = thin_border

        for c in range(2, 4):
            ws.cell(row=current_row, column=c).border = thin_border

        total_studs = len(df)
        for s_idx, s in enumerate(sessions):
            col_idx = 4 + s_idx
            pres_cnt = (df[s['header']] == "P").sum()
            rate = (pres_cnt / total_studs * 100.0) if total_studs > 0 else 0.0
            c_rate = ws.cell(row=current_row, column=col_idx, value=f"{rate:.0f}%")
            c_rate.font = font_cell_bold
            c_rate.alignment = align_center
            c_rate.border = thin_border
            c_rate.fill = fill_meta

        for c in range(4 + session_count, total_cols + 1):
            ws.cell(row=current_row, column=c).border = thin_border
            ws.cell(row=current_row, column=c).fill = fill_meta

        current_row += 1

    # 6. Academic Regulation Note & Official Signatures
    current_row += 2
    ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=total_cols)
    note_cell = ws.cell(row=current_row, column=1)
    note_cell.value = "📌 NOTE: Minimum 75% attendance is mandatory to appear for the Semester End Examinations as per College Regulations."
    note_cell.font = Font(name="Calibri", size=9, italic=True, color="64748B")
    note_cell.alignment = align_left

    current_row += 3
    # Faculty Signature (Left)
    sig_col_left = 2
    ws.cell(row=current_row, column=sig_col_left, value="Signature of Subject Faculty: _______________________").font = font_cell_bold

    # HOD Signature (Right)
    sig_col_right = max(5, total_cols - 3)
    ws.cell(row=current_row, column=sig_col_right, value="Signature of Head of Department: _______________________").font = font_cell_bold

    # 7. Auto-fit column widths with padding
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            # Skip title banner rows when calculating width
            if cell.row in (1, 2, 3, 4, 5, current_row - 3, current_row):
                continue
            val_str = str(cell.value or '')
            max_len = max(max_len, len(val_str))
        
        # Column specific minimums
        if col[0].column == 1:
            ws.column_dimensions[col_letter].width = 8
        elif col[0].column == 2:
            ws.column_dimensions[col_letter].width = 16
        elif col[0].column == 3:
            ws.column_dimensions[col_letter].width = 24
        else:
            ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    # 8. Freeze Panes: Lock Sr No, Roll No, Student Name (freeze at D8)
    ws.freeze_panes = "D8"

    # Export to memory buffer
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

