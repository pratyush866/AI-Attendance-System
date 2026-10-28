# Backup SnapClass tables to JSON files
# This script uses the Supabase Python client to export the five core tables.
# It reads SUPABASE_URL and SUPABASE_KEY from the existing .env file.
# The output JSON files are written to the project root for easy inspection.

import os
import json
from pathlib import Path
from dotenv import load_dotenv

try:
    from supabase import create_client, Client
except ImportError:
    raise ImportError("Supabase client not installed. Install with 'pip install supabase' or check requirements.")

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
if not url or not key:
    raise EnvironmentError("SUPABASE_URL or SUPABASE_KEY missing in .env")

supabase: Client = create_client(url, key)

# List of tables to back up
tables = ["teachers", "students", "subjects", "subject_students", "attendance_logs"]
output_dir = Path(__file__).parent.parent  # project root

for table in tables:
    # Supabase REST API: select all rows
    resp = supabase.table(table).select("*").execute()
    if resp.error:
        print(f"[ERROR] Failed to fetch {table}: {resp.error.message}")
        continue
    data = resp.data
    out_path = output_dir / f"backup_{table}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Backup {table} -> {out_path}")

print("All backups completed.")

