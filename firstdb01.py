import streamlit as st
import requests

url = st.secrets["SUPABASE_URL"].rstrip('/')
key = st.secrets["SUPABASE_KEY"]

st.title("Test via directe HTTP request")

# Maak de headers voor Supabase REST API
headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}"
}

# Vraag direct de data op via de PostgREST endpoint
api_url = f"{url}/rest/v1/gebruikers?select=*"

try:
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        st.success("Verbinding via HTTP werkt wél!")
        st.json(response.json())
    else:
        st.error(f"HTTP Foutcode {response.status_code}: {response.text}")

except Exception as e:
    st.error(f"Fout: {e}")
