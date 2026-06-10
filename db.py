import streamlit as st
from supabase import create_client, Client
import uuid

@st.cache_resource
def init_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return None

def save_simulation(champion, runner_up, third_place, user_name="Anonymous"):
    supabase: Client = init_supabase()
    if not supabase:
        return False
        
    try:
        data = {
            "champion": champion,
            "runner_up": runner_up,
            "third_place": third_place,
            "user_name": user_name
        }
        supabase.table("simulations").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving simulation: {e}")
        return False
