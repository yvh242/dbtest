import pandas as pd
import requests
import streamlit as st

url = st.secrets["SUPABASE_URL"].rstrip("/")
key = st.secrets["SUPABASE_KEY"]

st.title("Supabase Beheer Paneel")

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation" 
}

table_name = st.text_input("Tabelnaam:", value="gebruikers")
api_url = f"{url}/rest/v1/{table_name}"

# --- FUNCTIES ---
def fetch_data():
    response = requests.get(f"{api_url}?select=*", headers=headers)
    return response.json() if response.status_code == 200 else None

# --- TOEVOEGEN ---
with st.expander("➕ Nieuw record toevoegen"):
    with st.form("add_form"):
        # Let op: Pas de velden aan naar jouw databasekolommen!
        # Hier gaan we uit van een tabel met 'naam' en 'email'
        new_name = st.text_input("Naam")
        new_email = st.text_input("Email")
        submitted = st.form_submit_button("Toevoegen")
        
        if submitted:
            payload = {"naam": new_name, "email": new_email}
            response = requests.post(api_url, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                st.success("Record toegevoegd!")
                st.rerun()
            else:
                st.error(f"Fout bij toevoegen: {response.text}")

# --- DATA WEERGEVEN & VERWIJDEREN ---
data = fetch_data()

if data:
    df = pd.DataFrame(data)
    st.subheader("Huidige data")
    
    # We tonen de data in een tabel
    # Voor verwijderen gebruiken we een kolom met buttons
    for index, row in df.iterrows():
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(f"{row.to_dict()}")
        
        # Verwijder actie (gebaseerd op een 'id' kolom in je tabel)
        if col2.button("🗑️ Verwijder", key=f"del_{row['id']}"):
            del_url = f"{api_url}?id=eq.{row['id']}"
            response = requests.delete(del_url, headers=headers)
            if response.status_code == 204:
                st.toast("Record verwijderd!")
                st.rerun()
            else:
                st.error(f"Verwijderen mislukt: {response.text}")
else:
    st.info("Geen data gevonden of tabel is leeg.")
