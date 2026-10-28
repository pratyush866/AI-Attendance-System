# Backup SnapClass tables to JSON files (v2)
# This script uses the Supabase Python client to export the core tables.
# It reads SUPABASE_URL and SUPABASE_KEY from the existing .env file.
# The JSON files are written to the project root (same level as app.py).

import os
import json
from pathlib import Path
from dotenv import load_dotenv

try:
    from supabase import create_client, Client
except ImportError as e:
    raise ImportError("Supabase client not installed. Run 'pip install supabase python-dotenv' first.")

# Load env variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise EnvironmentError("SUPABASE_URL or SUPABASE_KEY missing in .env")

supabase: Client = create_client(url, key)

tables = ["teachers", "students", "subjects", "subject_students", "attendance_logs"]
output_dir = Path(__file__).resolve().parents[1]  # project root

for table in tables:
    # Fetch all rows via REST API
    resp = supabase.table(table).select("*").execute()
    # supabase returns a dict-like APIResponse with .data attribute
    data = getattr(resp, "data", None)
    if data is None:
        print(f"[WARN] No data returned for {table}. Skipping.")
        continue
    out_path = output_dir / f"backup_{table}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Backup {table} -> {out_path}")

print("All backups completed.")

