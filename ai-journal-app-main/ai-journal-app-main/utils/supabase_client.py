import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_secret(key):
    try:
        return st.secrets[key]
    except:
        return os.getenv(key)

url = get_secret("SUPABASE_URL")
key = get_secret("SUPABASE_ANON_KEY")

supabase: Client = create_client(url, key)