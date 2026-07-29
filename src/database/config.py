import os
import streamlit as st

try:
    from supabase import create_client, Client
except Exception:  # pragma: no cover - optional dependency fallback
    create_client = None
    Client = object


class _MissingSupabase:
    def table(self, *_args, **_kwargs):
        raise RuntimeError("Supabase is not configured. Add your credentials to Streamlit secrets or environment variables.")


def _build_client():
    if create_client is None:
        return _MissingSupabase()

    url = os.getenv("SUPABASE_URL") or os.getenv("supabase_url")
    key = os.getenv("SUPABASE_KEY") or os.getenv("supabase_key")

    if not url:
        try:
            url = st.secrets["supabase_url"]
        except Exception:
            url = ""

    if not key:
        try:
            key = st.secrets["supabase_key"]
        except Exception:
            key = ""

    if not url or not key:
        return _MissingSupabase()

    return create_client(url, key)


supabase: Client = _build_client())