import pandas as pd
import requests
import streamlit as st

# Pagina instellen voor mobiel (breedte zo optimaal mogelijk benutten)
st.set_page_config(page_title="Boodschappen", page_icon="🛒", layout="centered")

url = st.secrets["SUPABASE_URL"].rstrip("/")
key = st.secrets["SUPABASE_KEY"]

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

table_name = "boodschappen"
api_url = f"{url}/rest/v1/{table_name}"


# --- FUNCTIES ---
def fetch_data():
  response = requests.get(f"{api_url}?select=*&order=id.asc", headers=headers)
  return response.json() if response.status_code == 200 else None


# --- MOBIELE HEADER ---
st.markdown(
    "<h2 style='text-align: center; margin-bottom: 20px;'>🛒 Boodschappen</h2>",
    unsafe_allow_html=True,
)

# --- INVOERSECTIE (Geoptimaliseerd voor duim-gebruik) ---
with st.form("add_form", clear_on_submit=True):
  # Op mobiel is het fijn als het invoerveld groot genoeg is
  new_name = st.text_input(
      "Nieuw item",
      label_visibility="collapsed",
      placeholder="Typ een boodschap...",
  )
  
  # Een brede toevoegknop werkt op een touchscreen veel fijner dan een smal plusje
  submitted = st.form_submit_button("➕ Voeg toe", use_container_width=True)

  if submitted:
    if new_name.strip() != "":
      payload = {"name": new_name, "completed": False}
      response = requests.post(api_url, headers=headers, json=payload)

      if response.status_code in [200, 201]:
        st.rerun()
      else:
        st.error(f"Fout bij toevoegen: {response.text}")
    else:
      st.warning("Vul alstublieft een naam in.")

st.write("")  # Kleine witruimte

# --- DATA WEERGEVEN & BEHEREN ---
data = fetch_data()

if data:
  st.markdown("### Nog te kopen:")
  for row in data:
    item_id = row["id"]
    item_name = row["name"]
    item_completed = row["completed"]

    # Gebruik containers om elk item visueel los te koppelen (handig op kleine schermen)
    with st.container(border=True):
      is_checked = st.checkbox(
          item_name, value=item_completed, key=f"check_{item_id}"
      )

      if is_checked != item_completed:
        if is_checked:
          del_url = f"{api_url}?id=eq.{item_id}"
          response = requests.delete(del_url, headers=headers)

          if response.status_code in [200, 204]:
            st.rerun()
          else:
            st.error(f"Verwijderen mislukt: {response.text}")
else:
  st.info("Je boodschappenlijst is leeg! Geniet van je vrije tijd 🎉")
