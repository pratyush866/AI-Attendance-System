"""
SnapClass - SQLite to Supabase Migration Utility
Migrates all local data (teachers, students, biometric embeddings, subjects, enrollments, attendance logs)
from attendance.db to your Supabase cloud database.

Usage:
    python migrate_sqlite_to_supabase.py
"""

import sqlite3
import json
import os
import sys

# Ensure pipelines module can be found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from pipelines.database.config import get_supabase_client, is_db_connected

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "attendance.db"))

def migrate():
    print("=" * 60)
    print("SnapClass -> SQLite to Supabase Migration Tool")
    print("=" * 60)

    if not is_db_connected():
        print("\n[ERROR] Supabase is NOT connected!")
        print("Please configure your SUPABASE_URL and SUPABASE_KEY in:")
        print("  - .streamlit/secrets.toml OR")
        print("  - .env file")
        print("\nAlso ensure you ran 'schema.sql' in your Supabase SQL Editor first.\n")
        sys.exit(1)

    client, _ = get_supabase_client()
    if not os.path.exists(DB_PATH):
        print(f"\n[ERROR] Local database file not found at: {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("\n[1/5] Migrating Teachers...")
    cur.execute("SELECT teacher_id, username, password, name, created_at FROM teachers")
    teachers = [dict(r) for r in cur.fetchall()]
    if teachers:
        for t in teachers:
            try:
                client.table("teachers").upsert(t, on_conflict="teacher_id").execute()
            except Exception as e:
                print(f"  Warning inserting teacher {t['username']}: {e}")
        print(f"  -> Migrated {len(teachers)} teachers.")
    else:
        print("  -> No teachers found to migrate.")

    print("\n[2/5] Migrating Students (with Face & Voice embeddings)...")
    cur.execute("SELECT student_id, name, roll_number, face_embedding, voice_embedding, created_at FROM students")
    students = [dict(r) for r in cur.fetchall()]
    if students:
        for s in students:
            # Parse JSON text into Python lists for Postgres float8[]
            if s.get("face_embedding") and isinstance(s["face_embedding"], str):
                try:
                    s["face_embedding"] = json.loads(s["face_embedding"])
                except Exception:
                    pass
            if s.get("voice_embedding") and isinstance(s["voice_embedding"], str):
                try:
                    s["voice_embedding"] = json.loads(s["voice_embedding"])
                except Exception:
                    pass
            try:
                client.table("students").upsert(s, on_conflict="student_id").execute()
            except Exception as e:
                print(f"  Warning inserting student {s['name']}: {e}")
        print(f"  -> Migrated {len(students)} students.")
    else:
        print("  -> No students found to migrate.")

    print("\n[3/5] Migrating Subjects...")
    cur.execute("SELECT subject_id, subject_code, name, section, teacher_id, created_at FROM subjects")
    subjects = [dict(r) for r in cur.fetchall()]
    if subjects:
        for sub in subjects:
            try:
                client.table("subjects").upsert(sub, on_conflict="subject_id").execute()
            except Exception as e:
                print(f"  Warning inserting subject {sub['subject_code']}: {e}")
        print(f"  -> Migrated {len(subjects)} subjects.")
    else:
        print("  -> No subjects found to migrate.")

    print("\n[4/5] Migrating Student Enrollments (subject_students)...")
    cur.execute("SELECT student_id, subject_id, created_at FROM subject_students")
    enrollments = [dict(r) for r in cur.fetchall()]
    if enrollments:
        for en in enrollments:
            try:
                client.table("subject_students").upsert(en, on_conflict="student_id,subject_id").execute()
            except Exception as e:
                print(f"  Warning inserting enrollment (student {en['student_id']}, subject {en['subject_id']}): {e}")
        print(f"  -> Migrated {len(enrollments)} enrollments.")
    else:
        print("  -> No enrollments found to migrate.")

    print("\n[5/5] Migrating Attendance Logs...")
    cur.execute("SELECT attendance_id, student_id, subject_id, timestamp, is_present, created_at FROM attendance_logs")
    logs = [dict(r) for r in cur.fetchall()]
    if logs:
        for l in logs:
            l["is_present"] = bool(l["is_present"])
            try:
                client.table("attendance_logs").upsert(l, on_conflict="attendance_id").execute()
            except Exception as e:
                print(f"  Warning inserting log {l.get('attendance_id')}: {e}")
        print(f"  -> Migrated {len(logs)} attendance logs.")
    else:
        print("  -> No attendance logs found to migrate.")

    conn.close()
    print("\n" + "=" * 60)
    print("Migration completed successfully! Your data is now live on Supabase.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    migrate()
