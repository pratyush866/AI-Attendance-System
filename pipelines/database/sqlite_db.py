import sqlite3
import json
import os
import bcrypt

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "attendance.db"))

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_sqlite_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_number TEXT DEFAULT NULL,
            name TEXT NOT NULL,
            face_embedding TEXT DEFAULT NULL,
            voice_embedding TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );


        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            section TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS subject_students (
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (student_id, subject_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS attendance_logs (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            is_present INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

# Initialize DB on load
init_sqlite_db()

def _hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def _check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except Exception:
        return False

# --- Teacher functions ---
def check_teacher_exists(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM teachers WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def create_teacher(username, password, name):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = _hash_pass(password)
    cursor.execute("INSERT INTO teachers (username, password, name) VALUES (?, ?, ?)", (username, hashed, name))
    conn.commit()
    teacher_id = cursor.lastrowid
    cursor.execute("SELECT * FROM teachers WHERE teacher_id = ?", (teacher_id,))
    row = cursor.fetchone()
    conn.close()
    return [dict(row)] if row else []

def teacher_login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        teacher = dict(row)
        if _check_pass(password, teacher.get("password", "")):
            return teacher
    return None

# --- Student functions ---
def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        if d.get("face_embedding"):
            try:
                d["face_embedding"] = json.loads(d["face_embedding"])
            except Exception:
                pass
        if d.get("voice_embedding"):
            try:
                d["voice_embedding"] = json.loads(d["voice_embedding"])
            except Exception:
                pass
        results.append(d)
    return results

def create_student(new_name, roll_number=None, face_embedding=None, voice_embedding=None):
    conn = get_connection()
    cursor = conn.cursor()
    face_str = json.dumps(face_embedding) if face_embedding is not None else None
    voice_str = json.dumps(voice_embedding) if voice_embedding is not None else None
    cursor.execute("INSERT INTO students (name, roll_number, face_embedding, voice_embedding) VALUES (?, ?, ?, ?)", (new_name, roll_number, face_str, voice_str))
    conn.commit()
    student_id = cursor.lastrowid
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["face_embedding"] = face_embedding
        d["voice_embedding"] = voice_embedding
        return [d]
    return []

def update_student(student_id, name, roll_number=None, face_embedding=None, voice_embedding=None):
    conn = get_connection()
    cursor = conn.cursor()
    face_str = json.dumps(face_embedding) if face_embedding is not None else None
    voice_str = json.dumps(voice_embedding) if voice_embedding is not None else None
    
    # Fetch existing row first to preserve unmodified fields
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        return []
    
    final_roll = roll_number if roll_number is not None else existing["roll_number"]
    final_face = face_str if face_embedding is not None else existing["face_embedding"]
    final_voice = voice_str if voice_embedding is not None else existing["voice_embedding"]
    
    cursor.execute("""
        UPDATE students 
        SET name = ?, roll_number = ?, face_embedding = ?, voice_embedding = ? 
        WHERE student_id = ?
    """, (name, final_roll, final_face, final_voice, student_id))
    conn.commit()
    cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        d = dict(row)
        if d.get("face_embedding"):
            try:
                d["face_embedding"] = json.loads(d["face_embedding"])
            except Exception:
                pass
        if d.get("voice_embedding"):
            try:
                d["voice_embedding"] = json.loads(d["voice_embedding"])
            except Exception:
                pass
        return [d]
    return []

# --- Subject functions ---
def create_subject(subject_code, name, section, teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO subjects (subject_code, name, section, teacher_id) VALUES (?, ?, ?, ?)",
                   (subject_code, name, section, teacher_id))
    conn.commit()
    subject_id = cursor.lastrowid
    cursor.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
    row = cursor.fetchone()
    conn.close()
    return [dict(row)] if row else []

def get_teacher_subjects(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects WHERE teacher_id = ?", (teacher_id,))
    subjects = [dict(r) for r in cursor.fetchall()]

    for sub in subjects:
        sid = sub["subject_id"]
        cursor.execute("SELECT COUNT(*) as count FROM subject_students WHERE subject_id = ?", (sid,))
        sub["total_students"] = cursor.fetchone()["count"]

        cursor.execute("SELECT DISTINCT timestamp FROM attendance_logs WHERE subject_id = ?", (sid,))
        sub["total_classes"] = len(cursor.fetchall())

    conn.close()
    return subjects

def get_subject_by_code(subject_code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subjects WHERE subject_code = ?", (subject_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_subject_by_id(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sub.*, t.name as teacher_name
        FROM subjects sub
        LEFT JOIN teachers t ON sub.teacher_id = t.teacher_id
        WHERE sub.subject_id = ?
    """, (subject_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_enrolled_students(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ss.student_id, ss.subject_id, s.name, s.roll_number, s.face_embedding, s.voice_embedding
        FROM subject_students ss
        JOIN students s ON ss.student_id = s.student_id
        WHERE ss.subject_id = ?
    """, (subject_id,))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        face_emb = None
        voice_emb = None
        if r["face_embedding"]:
            try:
                face_emb = json.loads(r["face_embedding"])
            except Exception:
                pass
        if r["voice_embedding"]:
            try:
                voice_emb = json.loads(r["voice_embedding"])
            except Exception:
                pass

        results.append({
            "student_id": r["student_id"],
            "subject_id": r["subject_id"],
            "students": {
                "student_id": r["student_id"],
                "name": r["name"],
                "roll_number": r["roll_number"],
                "face_embedding": face_emb,
                "voice_embedding": voice_emb
            }
        })
    return results

def is_student_enrolled_in_subject(student_id, subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM subject_students WHERE student_id = ? AND subject_id = ?", (student_id, subject_id))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def enroll_student_to_subject(student_id, subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO subject_students (student_id, subject_id) VALUES (?, ?)", (student_id, subject_id))
    conn.commit()
    conn.close()
    return [{"student_id": student_id, "subject_id": subject_id}]

def unenroll_student_to_subject(student_id, subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM subject_students WHERE student_id = ? AND subject_id = ?", (student_id, subject_id))
    conn.commit()
    conn.close()
    return []

def get_student_subjects(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ss.student_id, ss.subject_id, sub.name, sub.subject_code, sub.section, sub.teacher_id
        FROM subject_students ss
        JOIN subjects sub ON ss.subject_id = sub.subject_id
        WHERE ss.student_id = ?
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()

    return [{
        "student_id": r["student_id"],
        "subject_id": r["subject_id"],
        "subjects": {
            "subject_id": r["subject_id"],
            "name": r["name"],
            "subject_code": r["subject_code"],
            "section": r["section"],
            "teacher_id": r["teacher_id"]
        }
    } for r in rows]

def get_student_attendance(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT al.attendance_id, al.student_id, al.subject_id, al.timestamp, al.is_present,
               sub.name, sub.subject_code
        FROM attendance_logs al
        JOIN subjects sub ON al.subject_id = sub.subject_id
        WHERE al.student_id = ?
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()

    return [{
        "attendance_id": r["attendance_id"],
        "student_id": r["student_id"],
        "subject_id": r["subject_id"],
        "timestamp": r["timestamp"],
        "is_present": bool(r["is_present"]),
        "subjects": {
            "name": r["name"],
            "subject_code": r["subject_code"]
        }
    } for r in rows]

def create_attendance(logs):
    if not logs:
        return []
    conn = get_connection()
    cursor = conn.cursor()
    for item in logs:
        cursor.execute("""
            INSERT INTO attendance_logs (student_id, subject_id, timestamp, is_present)
            VALUES (?, ?, ?, ?)
        """, (item["student_id"], item["subject_id"], item["timestamp"], 1 if item["is_present"] else 0))
    conn.commit()
    conn.close()
    return logs

def get_attendance_for_teacher(teacher_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT al.attendance_id, al.student_id, al.subject_id, al.timestamp, al.is_present,
               s.name as student_name, s.roll_number as student_roll_number, sub.name as subject_name, sub.subject_code
        FROM attendance_logs al
        JOIN subjects sub ON al.subject_id = sub.subject_id
        JOIN students s ON al.student_id = s.student_id
        WHERE sub.teacher_id = ?
    """, (teacher_id,))
    rows = cursor.fetchall()
    conn.close()

    return [{
        "attendance_id": r["attendance_id"],
        "student_id": r["student_id"],
        "subject_id": r["subject_id"],
        "timestamp": r["timestamp"],
        "is_present": bool(r["is_present"]),
        "students": {
            "student_id": r["student_id"],
            "name": r["student_name"],
            "roll_number": r["student_roll_number"]
        },
        "subjects": {
            "subject_id": r["subject_id"],
            "name": r["subject_name"],
            "subject_code": r["subject_code"],
            "teacher_id": teacher_id
        }
    } for r in rows]

def get_attendance_for_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT al.attendance_id, al.student_id, al.subject_id, al.timestamp, al.is_present,
               s.name as student_name, s.roll_number as student_roll_number
        FROM attendance_logs al
        JOIN students s ON al.student_id = s.student_id
        WHERE al.subject_id = ?
        ORDER BY al.timestamp ASC
    """, (subject_id,))
    rows = cursor.fetchall()
    conn.close()

    return [{
        "attendance_id": r["attendance_id"],
        "student_id": r["student_id"],
        "subject_id": r["subject_id"],
        "timestamp": r["timestamp"],
        "is_present": bool(r["is_present"]),
        "students": {
            "student_id": r["student_id"],
            "name": r["student_name"],
            "roll_number": r["student_roll_number"]
        }
    } for r in rows]


