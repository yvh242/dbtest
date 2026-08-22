import pandas as pd
import requests
import streamlit as st

url = st.secrets["SUPABASE_URL"].rstrip("/")
key = st.secrets["SUPABASE_KEY"]

st.title("Boodschappen")

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


# --- TOEVOEGEN ---
with st.form("add_form", clear_on_submit=True):
  col_input, col_btn = st.columns([0.85, 0.15])
  new_name = col_input.text_input(
      "Nieuw boodschap item:", label_visibility="collapsed", placeholder="Nieuw item..."
  )
  submitted = col_btn.form_submit_button("➕")

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

st.divider()

# --- DATA WEERGEVEN & BEHEREN VIA CHECKBOX ---
data = fetch_data()

if data:
  for row in data:
    item_id = row["id"]
    item_name = row["name"]
    item_completed = row["completed"]

    # Maak een checkbox. Zodra deze aangevinkt wordt, verdwijnt het item direct
    is_checked = st.checkbox(
        item_name, value=item_completed, key=f"check_{item_id}"
    )

    if is_checked != item_completed:
      if is_checked:  # Vinkje aangezet -> Direct verwijderen zonder melding
        del_url = f"{api_url}?id=eq.{item_id}"
        response = requests.delete(del_url, headers=headers)

        if response.status_code in [200, 204]:
          st.rerun()
        else:
          st.error(f"Verwijderen mislukt: {response.text}")
else:
  st.info("Je boodschappenlijst is momenteel leeg!")
