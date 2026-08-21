import pandas as pd
import requests
import streamlit as st

url = st.secrets["SUPABASE_URL"].rstrip("/")
key = st.secrets["SUPABASE_KEY"]

st.title("Supabase Database Viewer")

# Maak de headers voor Supabase REST API
headers = {"apikey": key, "Authorization": f"Bearer {key}"}

# Laat de gebruiker zelf de tabelnaam invullen (bijv. 'gebruikers')
table_name = st.text_input(
    "Naam van de tabel die je wilt bekijken:", value="gebruikers"
)

api_url = f"{url}/rest/v1/{table_name}?select=*"

if st.button("Laad Data"):
  try:
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
      data = response.json()

      if data:
        st.success(f"Tabel '{table_name}' succesvol geladen ({len(data)} rijen)!")

        # Converteer de JSON data naar een Pandas DataFrame
        df = pd.DataFrame(data)

        # Toon een interactieve, sorteerbare tabel
        st.dataframe(df, use_container_width=True)

        # Optioneel: Toon ook wat statistieken of ruwe data
        with st.expander("Bekijk als ruwe JSON"):
          st.json(data)
      else:
        st.warning(f"De tabel '{table_name}' is momenteel leeg.")

    else:
      st.error(f"HTTP Foutcode {response.status_code}: {response.text}")

  except Exception as e:
    st.error(f"Er is een fout opgetreden: {e}")
