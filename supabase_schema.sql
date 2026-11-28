-- SNAPCLASS / AI Attendance System — Complete Supabase PostgreSQL Schema
-- Paste and run this entire script once in your Supabase SQL Editor to make
-- attendance permanent across all teachers, students, and devices on Streamlit Cloud.

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    student_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    roll_no TEXT,
    face_embedding JSONB,
    voice_embedding JSONB
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id BIGSERIAL PRIMARY KEY,
    subject_code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    section TEXT NOT NULL,
    teacher_id BIGINT NOT NULL REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subject_students (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id BIGINT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE(student_id, subject_id)
);

CREATE TABLE IF NOT EXISTS attendance_sessions (
    session_id TEXT PRIMARY KEY,
    subject_id BIGINT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    teacher_id BIGINT NOT NULL REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    session_pin TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS session_selfies (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES attendance_sessions(session_id) ON DELETE CASCADE,
    student_id BIGINT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    timestamp TEXT NOT NULL,
    photo_verified BOOLEAN DEFAULT TRUE,
    similarity_score DOUBLE PRECISION DEFAULT 1.0,
    UNIQUE(session_id, student_id)
);

CREATE TABLE IF NOT EXISTS attendance_logs (
    id BIGSERIAL PRIMARY KEY,
    student_id BIGINT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id BIGINT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    session_id TEXT,
    timestamp TEXT NOT NULL,
    is_present BOOLEAN NOT NULL,
    verification_status TEXT DEFAULT 'Verified'
);
