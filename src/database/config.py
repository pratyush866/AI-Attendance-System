import streamlit as st
from supabase import create_client, Client
import os
import logging
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Fallbacks for Supabase configuration parameters
supabase_url = None
supabase_key = None

try:
    if hasattr(st, "secrets"):
        supabase_url = st.secrets.get("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY")
except Exception:
    pass

if not supabase_url:
    supabase_url = os.environ.get("SUPABASE_URL")
if not supabase_key:
    supabase_key = os.environ.get("SUPABASE_KEY")

supabase: Client = None
IS_SUPABASE_AVAILABLE = False

try:
    if supabase_url and supabase_key and str(supabase_url).startswith("http"):
        # Test if it's not a dummy URL
        if "dummy" not in str(supabase_url).lower():
            supabase = create_client(supabase_url, supabase_key)
            IS_SUPABASE_AVAILABLE = True
            logging.info("Connected to Supabase cloud successfully.")
        else:
            logging.info("Dummy Supabase URL detected, will use local high-performance SQLite engine.")
    else:
        logging.info("Supabase not configured or invalid URL. Using local high-performance SQLite engine.")
except Exception as e:
    logging.warning(f"Supabase connection notice: {e}. Falling back to local engine.")
    supabase = None
    IS_SUPABASE_AVAILABLE = False
