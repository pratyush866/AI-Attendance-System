import os
import streamlit as st

try:
    from supabase import create_client, Client
except Exception:
    create_client = None
    Client = object

def _get_secret(key, default=""):
    # 1. Check OS Environment Variables
    val = os.getenv(key)
    if val:
        return val.strip()

    # 2. Check Streamlit Secrets (.streamlit/secrets.toml)
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass

    # 3. Check local .env file as fallback
    try:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        env_path = os.path.join(root_dir, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() == key:
                            return v.strip().strip('"').strip("'")
    except Exception:
        pass

    return default

def get_supabase_client():
    """Dynamically retrieves and initializes the Supabase client."""
    url = _get_secret("SUPABASE_URL", "")
    key = _get_secret("SUPABASE_KEY", "")

    is_placeholder = (
        not url
        or not key
        or "your-project" in url
        or "your-supabase" in url
        or "your-anon" in key
        or "your-supabase-key" in key
    )

    if is_placeholder or create_client is None:
        return None, True

    try:
        client = create_client(url, key)
        return client, False
    except Exception as e:
        print(f"[Supabase Client Init Error]: {e}")
        return None, True

SUPABASE_URL = _get_secret("SUPABASE_URL", "")
SUPABASE_KEY = _get_secret("SUPABASE_KEY", "")
supabase, is_placeholder = get_supabase_client()

def is_db_connected():
    """Returns True if a valid Supabase client is initialized and reachable."""
    client, placeholder = get_supabase_client()
    return client is not None and not placeholder

