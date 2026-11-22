import os
import json
import sqlite3
import logging
import bcrypt
from datetime import datetime
import streamlit as st
from src.database.config import supabase, IS_SUPABASE_AVAILABLE

# Setup error logging
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "error.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Local SQLite Database Setup
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "college_attendance.db")


def get_local_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_local_db():
    conn = get_local_conn()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT,
            face_embedding TEXT,
            voice_embedding TEXT
        );

        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            section TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        );

        CREATE TABLE IF NOT EXISTS subject_students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            UNIQUE(student_id, subject_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        );

        CREATE TABLE IF NOT EXISTS attendance_sessions (
            session_id TEXT PRIMARY KEY,
            subject_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            session_pin TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        );

        CREATE TABLE IF NOT EXISTS session_selfies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            student_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            photo_verified INTEGER DEFAULT 1,
            similarity_score REAL DEFAULT 1.0,
            UNIQUE(session_id, student_id),
            FOREIGN KEY (session_id) REFERENCES attendance_sessions(session_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );

        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            session_id TEXT,
            timestamp TEXT NOT NULL,
            is_present INTEGER NOT NULL,
            verification_status TEXT DEFAULT 'Verified',
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        );
    """)

    # Check if default teacher exists, if not seed demo teacher
    cursor.execute("SELECT count(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        demo_pass = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)",
            ("prof_roy", demo_pass, "Prof. Ananya Roy")
        )
        teacher_id = cursor.lastrowid
        # Seed demo subject
        cursor.execute(
            "INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
            ("CS101", "Artificial Intelligence & ML", "Section A", teacher_id)
        )
        sub_id = cursor.lastrowid

        # Seed sample students (Akash, Priya, Rohan)
        sample_students = [
            ("Akash Sharma", "101"),
            ("Priya Verma", "102"),
            ("Rohan Gupta", "103"),
            ("Neha Singh", "104"),
            ("Amit Patel", "105")
        ]
        for s_name, s_roll in sample_students:
            cursor.execute(
                "INSERT INTO students (name, roll_no) VALUES (?, ?)",
                (s_name, s_roll)
            )
            s_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO subject_students (student_id, subject_id) VALUES (?, ?)",
                (s_id, sub_id)
            )

    conn.commit()
    conn.close()

# Initialize DB at module import
init_local_db()


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()


def check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except Exception:
        return False


def check_teacher_exists(username):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table("teachers").select("username").eq("username", username).execute()
            return len(res.data) > 0
        except Exception as e:
            logging.warning(f"Supabase error, fallback to local: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("SELECT 1 FROM teachers WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row is not None


def create_teacher(username, password, name):
    hashed = hash_pass(password)
    if IS_SUPABASE_AVAILABLE:
        try:
            data = {"username": username, "password": hashed, "name": name}
            res = supabase.table("teachers").insert(data).execute()
            return res.data
        except Exception as e:
            logging.warning(f"Supabase insert failed, fallback to local: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)", (username, hashed, name))
    tid = c.lastrowid
    conn.commit()
    c.execute("SELECT * FROM teachers WHERE teacher_id = ?", (tid,))
    row = dict(c.fetchone())
    conn.close()
    return [row]


def teacher_login(username, password):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table("teachers").select("*").eq("username", username).execute()
            if res.data:
                teacher = res.data[0]
                if check_pass(password, teacher['password']):
                    return teacher
        except Exception as e:
            logging.warning(f"Supabase login failed, fallback to local: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row:
        teacher = dict(row)
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('students').select("*").execute()
            if res.data is not None:
                return res.data
        except Exception as e:
            logging.warning(f"Supabase get_all_students failed, fallback to local: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    for r in rows:
        if r.get('face_embedding') and isinstance(r['face_embedding'], str):
            try:
                r['face_embedding'] = json.loads(r['face_embedding'])
            except Exception:
                pass
        if r.get('voice_embedding') and isinstance(r['voice_embedding'], str):
            try:
                r['voice_embedding'] = json.loads(r['voice_embedding'])
            except Exception:
                pass
    return rows


def create_student(new_name, roll_no=None, face_embedding=None, voice_embedding=None):
    face_json = json.dumps(face_embedding) if face_embedding is not None else None
    voice_json = json.dumps(voice_embedding) if voice_embedding is not None else None

    if IS_SUPABASE_AVAILABLE:
        try:
            data = {'name': new_name, 'face_embedding': face_embedding, "voice_embedding": voice_embedding}
            res = supabase.table('students').insert(data).execute()
            return res.data
        except Exception as e:
            logging.warning(f"Supabase create_student failed, fallback to local: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (name, roll_no, face_embedding, voice_embedding) VALUES (?, ?, ?, ?)",
        (new_name, roll_no, face_json, voice_json)
    )
    sid = c.lastrowid
    conn.commit()
    c.execute("SELECT * FROM students WHERE student_id = ?", (sid,))
    row = dict(c.fetchone())
    conn.close()
    if row.get('face_embedding'):
        row['face_embedding'] = face_embedding
    if row.get('voice_embedding'):
        row['voice_embedding'] = voice_embedding
    return [row]


def create_subject(subject_code, name, section, teacher_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
            res = supabase.table("subjects").insert(data).execute()
            return res.data
        except Exception as e:
            logging.warning(f"Supabase create_subject failed, fallback to local: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
        (subject_code, name, section, teacher_id)
    )
    sub_id = c.lastrowid
    conn.commit()
    c.execute("SELECT * FROM subjects WHERE subject_id = ?", (sub_id,))
    row = dict(c.fetchone())
    conn.close()
    return [row]


def get_teacher_subjects(teacher_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
            subjects = res.data
            for sub in subjects:
                sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
                attendance = sub.get('attendance_logs', [])
                unique_sessions = len(set(log['timestamp'] for log in attendance))
                sub['total_classes'] = unique_sessions
                sub.pop('subject_students', None)
                sub.pop('attendance_logs', None)
            return subjects
        except Exception as e:
            logging.warning(f"Supabase get_teacher_subjects failed: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT s.*, 
               (SELECT COUNT(*) FROM subject_students ss WHERE ss.subject_id = s.subject_id) AS total_students,
               (SELECT COUNT(DISTINCT timestamp) FROM attendance_logs al WHERE al.subject_id = s.subject_id) AS total_classes
        FROM subjects s
        WHERE s.teacher_id = ?
    """, (teacher_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def enroll_student_to_subject(student_id, subject_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            data = {'student_id': student_id, "subject_id": subject_id}
            res = supabase.table('subject_students').insert(data).execute()
            return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO subject_students (student_id, subject_id) VALUES (?, ?)", (student_id, subject_id))
        conn.commit()
    finally:
        conn.close()
    return [{"student_id": student_id, "subject_id": subject_id}]


def unenroll_student_to_subject(student_id, subject_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
            return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("DELETE FROM subject_students WHERE student_id = ? AND subject_id = ?", (student_id, subject_id))
    conn.commit()
    conn.close()
    return [{"status": "success"}]


def get_student_subjects(student_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
            if res.data:
                return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT ss.id, ss.student_id, ss.subject_id,
               s.name, s.subject_code, s.section, s.teacher_id
        FROM subject_students ss
        JOIN subjects s ON ss.subject_id = s.subject_id
        WHERE ss.student_id = ?
    """, (student_id,))
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            'student_id': r['student_id'],
            'subject_id': r['subject_id'],
            'subjects': {
                'subject_id': r['subject_id'],
                'name': r['name'],
                'subject_code': r['subject_code'],
                'section': r['section'],
                'teacher_id': r['teacher_id']
            }
        })
    return result


def get_student_attendance(student_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
            if res.data:
                return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT al.*, s.name, s.subject_code, s.section
        FROM attendance_logs al
        JOIN subjects s ON al.subject_id = s.subject_id
        WHERE al.student_id = ?
    """, (student_id,))
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            'id': r['id'],
            'student_id': r['student_id'],
            'subject_id': r['subject_id'],
            'timestamp': r['timestamp'],
            'is_present': bool(r['is_present']),
            'verification_status': r['verification_status'],
            'subjects': {
                'name': r['name'],
                'subject_code': r['subject_code'],
                'section': r['section']
            }
        })
    return result


def create_attendance(logs):
    if not logs:
        return []
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('attendance_logs').insert(logs).execute()
            return res.data
        except Exception as e:
            logging.warning(f"Supabase create_attendance error: {e}")

    conn = get_local_conn()
    c = conn.cursor()
    for log in logs:
        c.execute("""
            INSERT INTO attendance_logs (student_id, subject_id, session_id, timestamp, is_present, verification_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            log['student_id'],
            log['subject_id'],
            log.get('session_id', ''),
            log['timestamp'],
            1 if log['is_present'] else 0,
            log.get('verification_status', 'Verified')
        ))
    conn.commit()
    conn.close()
    return logs


def get_attendance_for_teacher(teacher_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('attendance_logs').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
            if res.data:
                return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT al.*, s.name AS subject_name, s.subject_code, s.section, s.teacher_id
        FROM attendance_logs al
        JOIN subjects s ON al.subject_id = s.subject_id
        WHERE s.teacher_id = ?
        ORDER BY al.timestamp DESC
    """, (teacher_id,))
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        result.append({
            'id': r['id'],
            'student_id': r['student_id'],
            'subject_id': r['subject_id'],
            'timestamp': r['timestamp'],
            'is_present': bool(r['is_present']),
            'verification_status': r['verification_status'],
            'subjects': {
                'subject_id': r['subject_id'],
                'name': r['subject_name'],
                'subject_code': r['subject_code'],
                'section': r['section'],
                'teacher_id': r['teacher_id']
            }
        })
    return result


def get_subject_students(subject_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute()
            if res.data:
                return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT ss.id, ss.student_id, ss.subject_id,
               st.name, st.roll_no, st.face_embedding, st.voice_embedding
        FROM subject_students ss
        JOIN students st ON ss.student_id = st.student_id
        WHERE ss.subject_id = ?
    """, (subject_id,))
    rows = c.fetchall()
    conn.close()
    result = []
    for r in rows:
        face_emb = r['face_embedding']
        if face_emb and isinstance(face_emb, str):
            try:
                face_emb = json.loads(face_emb)
            except Exception:
                pass
        voice_emb = r['voice_embedding']
        if voice_emb and isinstance(voice_emb, str):
            try:
                voice_emb = json.loads(voice_emb)
            except Exception:
                pass

        result.append({
            'id': r['id'],
            'student_id': r['student_id'],
            'subject_id': r['subject_id'],
            'students': {
                'student_id': r['student_id'],
                'name': r['name'],
                'roll_no': r['roll_no'],
                'face_embedding': face_emb,
                'voice_embedding': voice_emb
            }
        })
    return result


def get_subject_by_code(subject_code):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('subjects').select('subject_id, name, subject_code, section').eq('subject_code', subject_code).execute()
            if res.data:
                return res.data
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM subjects WHERE subject_code = ?", (subject_code,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def check_enrollment_exists(student_id, subject_id):
    if IS_SUPABASE_AVAILABLE:
        try:
            res = supabase.table('subject_students').select('*').eq('subject_id', subject_id).eq('student_id', student_id).execute()
            return len(res.data) > 0
        except Exception:
            pass

    conn = get_local_conn()
    c = conn.cursor()
    c.execute("SELECT 1 FROM subject_students WHERE student_id = ? AND subject_id = ?", (student_id, subject_id))
    row = c.fetchone()
    conn.close()
    return row is not None


# ==========================================
# DUAL-VERIFICATION ATTENDANCE SESSION API
# ==========================================

def create_attendance_session(subject_id, teacher_id, session_pin):
    import uuid
    session_id = str(uuid.uuid4())[:8].upper()
    created_at = datetime.now().isoformat()

    conn = get_local_conn()
    c = conn.cursor()
    # Close any existing active sessions for this subject
    c.execute("UPDATE attendance_sessions SET status = 'closed' WHERE subject_id = ? AND status = 'active'", (subject_id,))
    c.execute("""
        INSERT INTO attendance_sessions (session_id, subject_id, teacher_id, session_pin, status, created_at)
        VALUES (?, ?, ?, ?, 'active', ?)
    """, (session_id, subject_id, teacher_id, str(session_pin), created_at))
    conn.commit()
    c.execute("SELECT * FROM attendance_sessions WHERE session_id = ?", (session_id,))
    row = dict(c.fetchone())
    conn.close()
    return row


def get_session_by_id(session_id):
    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT sess.*, s.name AS subject_name, s.subject_code, s.section, t.name AS teacher_name
        FROM attendance_sessions sess
        JOIN subjects s ON sess.subject_id = s.subject_id
        JOIN teachers t ON sess.teacher_id = t.teacher_id
        WHERE sess.session_id = ?
    """, (session_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def submit_session_selfie(session_id, student_id, similarity_score=1.0):
    timestamp = datetime.now().isoformat()
    conn = get_local_conn()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO session_selfies (session_id, student_id, timestamp, photo_verified, similarity_score)
            VALUES (?, ?, ?, 1, ?)
            ON CONFLICT(session_id, student_id) DO UPDATE SET 
                timestamp = excluded.timestamp,
                similarity_score = excluded.similarity_score
        """, (session_id, student_id, timestamp, similarity_score))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f"Error submitting session selfie: {e}")
        return False
    finally:
        conn.close()


def get_session_selfies(session_id):
    conn = get_local_conn()
    c = conn.cursor()
    c.execute("""
        SELECT ss.*, st.name AS student_name, st.roll_no
        FROM session_selfies ss
        JOIN students st ON ss.student_id = st.student_id
        WHERE ss.session_id = ?
        ORDER BY ss.timestamp ASC
    """, (session_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def close_attendance_session(session_id):
    conn = get_local_conn()
    c = conn.cursor()
    c.execute("UPDATE attendance_sessions SET status = 'closed' WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()
