from pipelines.database.config import get_supabase_client, is_db_connected
import pipelines.database.sqlite_db as sqlite_db
import bcrypt
import json

def _get_active_client():
    client, is_dummy = get_supabase_client()
    return client if (client is not None and not is_dummy) else None

def _safe_execute(fn):
    client = _get_active_client()
    if client is None:
        return type('Resp', (), {'data': []})()
    try:
        return fn(client)
    except Exception as e:
        print(f"[Supabase Database Error]: {e}")
        return type('Resp', (), {'data': []})()

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except Exception:
        return False

# --- Teacher functions ---
def check_teacher_exists(username):
    if not is_db_connected():
        return sqlite_db.check_teacher_exists(username)
    response = _safe_execute(lambda client: client.table("teachers").select("username").eq("username", username).execute())
    return len(getattr(response, 'data', [])) > 0

def create_teacher(username, password, name):
    if not is_db_connected():
        return sqlite_db.create_teacher(username, password, name)
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = _safe_execute(lambda client: client.table("teachers").insert(data).execute())
    return getattr(response, 'data', [])

def teacher_login(username, password):
    """Authenticate a teacher.

    Preference order:
    1. If Supabase Auth session is available, use the `auth_uid` mapping.
    2. Fallback to legacy username/password check (hashed password).
    """
    if not is_db_connected():
        return sqlite_db.teacher_login(username, password)
    # Attempt Supabase Auth UID based login
    client = _get_active_client()
    if client is not None:
        try:
            # Retrieve currently authenticated user UID
            auth_resp = client.auth.get_user()
            uid = getattr(getattr(auth_resp, 'data', None), 'user', None)
            # Supabase Python client may return a dict-like object; handle both
            if isinstance(uid, dict):
                uid = uid.get('id')
            elif hasattr(uid, 'id'):
                uid = uid.id
            if uid:
                resp = _safe_execute(lambda c: c.table("teachers").select("*").eq("auth_uid", uid).single().execute())
                teacher = getattr(resp, 'data', None)
                if teacher:
                    return teacher
        except Exception as e:
            print(f"[Supabase Auth UID login error]: {e}")
    # Fallback to legacy username/password login
    response = _safe_execute(lambda client: client.table("teachers").select("*").eq("username", username).execute())
    data = getattr(response, 'data', None)
    if data and len(data) > 0:
        teacher = data[0]
        if check_pass(password, teacher.get('password', '')):
            return teacher
    return None


# --- Student functions ---
def get_all_students():
    if not is_db_connected():
        return sqlite_db.get_all_students()
    response = _safe_execute(lambda client: client.table('students').select("*").execute())
    data = getattr(response, 'data', [])
    for s in data:
        if isinstance(s.get("face_embedding"), str):
            try:
                s["face_embedding"] = json.loads(s["face_embedding"])
            except Exception:
                pass
        if isinstance(s.get("voice_embedding"), str):
            try:
                s["voice_embedding"] = json.loads(s["voice_embedding"])
            except Exception:
                pass
    return data

def create_student(new_name, roll_number=None, face_embedding=None, voice_embedding=None):
    if not is_db_connected():
        return sqlite_db.create_student(new_name, roll_number=roll_number, face_embedding=face_embedding, voice_embedding=voice_embedding)
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
    if roll_number is not None:
        data['roll_number'] = roll_number
    response = _safe_execute(lambda client: client.table('students').insert(data).execute())
    data_res = getattr(response, 'data', [])
    if not data_res and 'roll_number' in data:
        # Graceful fallback if roll_number column not yet migrated in Supabase
        fallback_data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embedding': voice_embedding}
        response = _safe_execute(lambda client: client.table('students').insert(fallback_data).execute())
        data_res = getattr(response, 'data', [])
    return data_res

def update_student(student_id, name, roll_number=None, face_embedding=None, voice_embedding=None):
    if not is_db_connected():
        return sqlite_db.update_student(student_id, name, roll_number=roll_number, face_embedding=face_embedding, voice_embedding=voice_embedding)
    data = {'name': name}
    if roll_number is not None:
        data['roll_number'] = roll_number
    if face_embedding is not None:
        data['face_embedding'] = face_embedding
    if voice_embedding is not None:
        data['voice_embedding'] = voice_embedding
    response = _safe_execute(lambda client: client.table('students').update(data).eq('student_id', student_id).execute())
    data_res = getattr(response, 'data', [])
    if not data_res and 'roll_number' in data:
        # Graceful fallback if roll_number column not yet migrated in Supabase
        fallback_data = {'name': name}
        if face_embedding is not None:
            fallback_data['face_embedding'] = face_embedding
        if voice_embedding is not None:
            fallback_data['voice_embedding'] = voice_embedding
        response = _safe_execute(lambda client: client.table('students').update(fallback_data).eq('student_id', student_id).execute())
        data_res = getattr(response, 'data', [])
    return data_res


# --- Subject functions ---
def create_subject(subject_code, name, section, teacher_id):
    if not is_db_connected():
        return sqlite_db.create_subject(subject_code, name, section, teacher_id)
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = _safe_execute(lambda client: client.table("subjects").insert(data).execute())
    return getattr(response, 'data', [])

def get_teacher_subjects(teacher_id):
    if not is_db_connected():
        return sqlite_db.get_teacher_subjects(teacher_id)
    response = _safe_execute(lambda client: client.table('subjects').select("*, subject_students(student_id), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute())
    subjects = getattr(response, 'data', [])

    for sub in subjects:
        sub['total_students'] = len(sub.get('subject_students', []))
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log.get('timestamp') for log in attendance if 'timestamp' in log))
        sub['total_classes'] = unique_sessions
        sub.pop('subject_students', None)
        sub.pop('attendance_logs', None)

    return subjects

def get_subject_by_code(subject_code):
    if not is_db_connected():
        return sqlite_db.get_subject_by_code(subject_code)
    response = _safe_execute(lambda client: client.table('subjects').select("subject_id, name, subject_code").eq('subject_code', subject_code).execute())
    data = getattr(response, 'data', [])
    return data[0] if data else None

def get_subject_by_id(subject_id):
    if not is_db_connected():
        return sqlite_db.get_subject_by_id(subject_id)
    response = _safe_execute(lambda client: client.table('subjects').select("*, teachers(name)").eq('subject_id', subject_id).execute())
    data = getattr(response, 'data', [])
    if data:
        sub = dict(data[0])
        if isinstance(sub.get('teachers'), list) and sub['teachers']:
            sub['teacher_name'] = sub['teachers'][0].get('name')
        elif isinstance(sub.get('teachers'), dict):
            sub['teacher_name'] = sub['teachers'].get('name')
        return sub
    return None

def get_enrolled_students(subject_id):
    if not is_db_connected():
        return sqlite_db.get_enrolled_students(subject_id)
    response = _safe_execute(lambda client: client.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute())
    data = getattr(response, 'data', [])
    normalized = []
    for row in data:
        r = dict(row)
        if isinstance(r.get('students'), list) and len(r['students']) > 0:
            r['students'] = r['students'][0]
        normalized.append(r)
    return normalized

def get_attendance_for_subject(subject_id):
    if not is_db_connected():
        return sqlite_db.get_attendance_for_subject(subject_id)
    response = _safe_execute(lambda client: client.table('attendance_logs').select("*, students(*)").eq('subject_id', subject_id).order('timestamp').execute())
    data = getattr(response, 'data', [])
    normalized = []
    for row in data:
        r = dict(row)
        if isinstance(r.get('students'), list) and len(r['students']) > 0:
            r['students'] = r['students'][0]
        normalized.append(r)
    return normalized

def is_student_enrolled_in_subject(student_id, subject_id):
    if not is_db_connected():
        return sqlite_db.is_student_enrolled_in_subject(student_id, subject_id)
    response = _safe_execute(lambda client: client.table('subject_students').select('*').eq('subject_id', subject_id).eq('student_id', student_id).execute())
    return len(getattr(response, 'data', [])) > 0

def enroll_student_to_subject(student_id, subject_id):
    if not is_db_connected():
        return sqlite_db.enroll_student_to_subject(student_id, subject_id)
    data = {'student_id': student_id, 'subject_id': subject_id}
    response = _safe_execute(lambda client: client.table('subject_students').insert(data).execute())
    return getattr(response, 'data', [])

def unenroll_student_to_subject(student_id, subject_id):
    if not is_db_connected():
        return sqlite_db.unenroll_student_to_subject(student_id, subject_id)
    response = _safe_execute(lambda client: client.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute())
    return getattr(response, 'data', [])

def get_student_subjects(student_id):
    if not is_db_connected():
        return sqlite_db.get_student_subjects(student_id)
    response = _safe_execute(lambda client: client.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute())
    data = getattr(response, 'data', [])
    normalized = []
    for row in data:
        r = dict(row)
        if isinstance(r.get('subjects'), list) and len(r['subjects']) > 0:
            r['subjects'] = r['subjects'][0]
        normalized.append(r)
    return normalized

def get_student_attendance(student_id):
    if not is_db_connected():
        return sqlite_db.get_student_attendance(student_id)
    response = _safe_execute(lambda client: client.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute())
    data = getattr(response, 'data', [])
    normalized = []
    for row in data:
        r = dict(row)
        if isinstance(r.get('subjects'), list) and len(r['subjects']) > 0:
            r['subjects'] = r['subjects'][0]
        normalized.append(r)
    return normalized

def create_attendance(logs):
    if not is_db_connected():
        return sqlite_db.create_attendance(logs)
    response = _safe_execute(lambda client: client.table('attendance_logs').insert(logs).execute())
    return getattr(response, 'data', [])

def get_attendance_for_teacher(teacher_id):
    if not is_db_connected():
        return sqlite_db.get_attendance_for_teacher(teacher_id)
    response = _safe_execute(lambda client: client.table('attendance_logs').select("*, subjects!inner(*), students(*)").eq('subjects.teacher_id', teacher_id).execute())
    data = getattr(response, 'data', [])
    normalized = []
    for row in data:
        r = dict(row)
        if isinstance(r.get('subjects'), list) and len(r['subjects']) > 0:
            r['subjects'] = r['subjects'][0]
        if isinstance(r.get('students'), list) and len(r['students']) > 0:
            r['students'] = r['students'][0]
        normalized.append(r)
    return normalized

def get_attendance_for_subject(subject_id):
    if not is_db_connected():
        return sqlite_db.get_attendance_for_subject(subject_id)
    response = _safe_execute(lambda client: client.table('attendance_logs').select("*, students(*)").eq('subject_id', subject_id).order('timestamp').execute())
    data = getattr(response, 'data', [])
    normalized = []
    for row in data:
        r = dict(row)
        if isinstance(r.get('students'), list) and len(r['students']) > 0:
            r['students'] = r['students'][0]
        normalized.append(r)
    return normalized