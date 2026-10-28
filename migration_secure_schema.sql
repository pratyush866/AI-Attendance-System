-- migration_secure_schema.sql
-- Revised migration for SnapClass Supabase schema hardening
-- Generated on 2026-10-28 by Antigravity (final revision)

-- ------------------------------------------------------------
-- 1. Add auth_uid column to teachers (UUID) and FK to auth.users(id)
-- ------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema='public' AND table_name='teachers' AND column_name='auth_uid'
    ) THEN
        ALTER TABLE public.teachers ADD COLUMN auth_uid UUID;
    END IF;
EXCEPTION WHEN duplicate_column THEN NULL; END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname='teachers_auth_uid_fkey' AND conrelid='public.teachers'::regclass
    ) THEN
        ALTER TABLE public.teachers
            ADD CONSTRAINT teachers_auth_uid_fkey FOREIGN KEY (auth_uid) REFERENCES auth.users(id) ON DELETE SET NULL;
    END IF;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ------------------------------------------------------------
-- 2. (Optional) Add auth_uid column to students (UUID) – currently omitted.
-- Uncomment the block below if student‑side Auth is required.
-- ------------------------------------------------------------
/*
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema='public' AND table_name='students' AND column_name='auth_uid'
    ) THEN
        ALTER TABLE public.students ADD COLUMN auth_uid UUID;
    END IF;
EXCEPTION WHEN duplicate_column THEN NULL; END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname='students_auth_uid_fkey' AND conrelid='public.students'::regclass
    ) THEN
        ALTER TABLE public.students
            ADD CONSTRAINT students_auth_uid_fkey FOREIGN KEY (auth_uid) REFERENCES auth.users(id) ON DELETE SET NULL;
    END IF;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;
*/

-- ------------------------------------------------------------
-- 3. Enable Row Level Security (RLS) on core tables
-- ------------------------------------------------------------
ALTER TABLE public.teachers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subject_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.attendance_logs ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------
-- 4. Drop known insecure policies (if they exist)
-- ------------------------------------------------------------
DROP POLICY IF EXISTS "Allow all on teachers" ON public.teachers;
DROP POLICY IF EXISTS "Allow all on students" ON public.students;
DROP POLICY IF EXISTS "Allow all on subjects" ON public.subjects;
DROP POLICY IF EXISTS "Allow all on subject_students" ON public.subject_students;
DROP POLICY IF EXISTS "Allow all on attendance_logs" ON public.attendance_logs;

-- ------------------------------------------------------------
-- 5. Create scoped RLS policies (idempotent)
-- ------------------------------------------------------------
-- Teachers: can SELECT, UPDATE, INSERT, DELETE their own rows; cannot change auth_uid to another UID.
DO $$ BEGIN
    CREATE POLICY teachers_self_select ON public.teachers
        FOR SELECT USING (auth_uid = auth.uid());
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY teachers_self_update ON public.teachers
        FOR UPDATE USING (auth_uid = auth.uid()) WITH CHECK (auth_uid = auth.uid());
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY teachers_self_insert ON public.teachers
        FOR INSERT WITH CHECK (auth_uid = auth.uid());
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY teachers_self_delete ON public.teachers
        FOR DELETE USING (auth_uid = auth.uid());
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Students: only teachers (authenticated) can manage student rows.
DO $$ BEGIN
    CREATE POLICY students_self_select ON public.students
        FOR SELECT USING (EXISTS (SELECT 1 FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY students_self_update ON public.students
        FOR UPDATE USING (EXISTS (SELECT 1 FROM public.teachers WHERE auth_uid = auth.uid()))
        WITH CHECK (EXISTS (SELECT 1 FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY students_self_insert ON public.students
        FOR INSERT WITH CHECK (EXISTS (SELECT 1 FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY students_self_delete ON public.students
        FOR DELETE USING (EXISTS (SELECT 1 FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Subjects: teachers manage subjects they own.
DO $$ BEGIN
    CREATE POLICY subjects_teacher_select ON public.subjects
        FOR SELECT USING (teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY subjects_teacher_update ON public.subjects
        FOR UPDATE USING (teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())) WITH CHECK (teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY subjects_teacher_insert ON public.subjects
        FOR INSERT WITH CHECK (teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY subjects_teacher_delete ON public.subjects
        FOR DELETE USING (teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid()));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Subject_Students: teachers manage enrollments for their subjects; students (if auth_uid added) could manage their own enrollments.
DO $$ BEGIN
    CREATE POLICY subject_students_teacher_select ON public.subject_students
        FOR SELECT USING (subject_id IN (SELECT subject_id FROM public.subjects WHERE teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY subject_students_teacher_insert ON public.subject_students
        FOR INSERT WITH CHECK (subject_id IN (SELECT subject_id FROM public.subjects WHERE teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY subject_students_teacher_delete ON public.subject_students
        FOR DELETE USING (subject_id IN (SELECT subject_id FROM public.subjects WHERE teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Attendance_Logs: teachers view/insert logs for their subjects; students could view own logs when auth_uid is present.
DO $$ BEGIN
    CREATE POLICY attendance_logs_teacher_select ON public.attendance_logs
        FOR SELECT USING (subject_id IN (SELECT subject_id FROM public.subjects WHERE teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY attendance_logs_teacher_insert ON public.attendance_logs
        FOR INSERT WITH CHECK (subject_id IN (SELECT subject_id FROM public.subjects WHERE teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE POLICY attendance_logs_teacher_delete ON public.attendance_logs
        FOR DELETE USING (subject_id IN (SELECT subject_id FROM public.subjects WHERE teacher_id = (SELECT teacher_id FROM public.teachers WHERE auth_uid = auth.uid())));
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ------------------------------------------------------------
-- 6. Adjust privileges (preserve service_role backend rights)
-- ------------------------------------------------------------
-- Revoke excessive rights from anonymous and authenticated roles; keep service_role untouched.
REVOKE ALL ON TABLE public.teachers FROM anon, authenticated;
REVOKE ALL ON TABLE public.students FROM anon, authenticated;
REVOKE ALL ON TABLE public.subjects FROM anon, authenticated;
REVOKE ALL ON TABLE public.subject_students FROM anon, authenticated;
REVOKE ALL ON TABLE public.attendance_logs FROM anon, authenticated;

-- Grant minimal CRUD rights to authenticated role (RLS will enforce row ownership).
GRANT SELECT, INSERT, UPDATE, DELETE ON public.teachers TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.students TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.subjects TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.subject_students TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.attendance_logs TO authenticated;

-- Service_role retains full privileges for backend operations (unchanged).

-- ------------------------------------------------------------
-- 7. Ensure sequences are owned by their tables (if they exist)
-- ------------------------------------------------------------
ALTER SEQUENCE IF EXISTS teachers_teacher_id_seq OWNED BY public.teachers.teacher_id;
ALTER SEQUENCE IF EXISTS students_student_id_seq OWNED BY public.students.student_id;
ALTER SEQUENCE IF EXISTS subjects_subject_id_seq OWNED BY public.subjects.subject_id;
ALTER SEQUENCE IF EXISTS attendance_logs_attendance_id_seq OWNED BY public.attendance_logs.attendance_id;

-- ------------------------------------------------------------
-- 8. Add unique indexes for critical columns (idempotent)
-- ------------------------------------------------------------
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM (
            SELECT username FROM public.teachers GROUP BY username HAVING COUNT(*) > 1
        ) AS dup
    ) THEN
        CREATE UNIQUE INDEX idx_teachers_username ON public.teachers(username);
    ELSE
        RAISE NOTICE 'Duplicate usernames exist – unique index not created. Resolve duplicates before enforcing uniqueness.';
    END IF;
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE UNIQUE INDEX IF NOT EXISTS idx_subjects_code ON public.subjects(subject_code);
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ------------------------------------------------------------
-- Migration complete.
-- After applying, you must:
--   1. Populate teachers.auth_uid with the correct Supabase Auth UID for each teacher.
--   2. If student authentication is later required, uncomment the student block above and populate auth_uid.
--   3. Update application code to use auth_uid for authentication (the fallback username/password still works).
--   4. Verify backups before proceeding.
--   5. Test RLS policies with multiple user accounts.
