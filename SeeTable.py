import streamlit as st
from supabase import create_client, Client

# 1. Verbinding maken met Supabase (haal je gegevens op uit je Supabase dashboard)
SUPABASE_URL = "JOUW_SUPABASE_URL"
SUPABASE_KEY = "JOUW_SUPABASE_ANON_KEY"

@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase: Client = init_connection()

# 2. Titel van de app
st.title("Boodschappen")

# 3. Item toevoegen met een '+' teken
with st.form(key="add_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        new_item = st.text_input("Nieuw item", placeholder="Typ een boodschap...", label_visibility="collapsed")
    with col2:
        submit = st.form_submit_button("+")
        
    if submit and new_item.strip():
        supabase.table("shopping_items").insert({"name": new_item.strip()}).execute()
        st.rerun()

# 4. Items ophalen uit de database
response = supabase.table("shopping_items").select("*").order("created_at", create_at_asc=False).execute()
items = response.data

st.divider()

# 5. Lijst tonen met afvink- en direct verwijderen-knop
if not items:
    st.info("Je lijstje is leeg!")
else:
    for item in items:
        col_check, col_del = st.columns([5, 1])
        
        with col_check:
            # Checkbox om af te vinken
            is_completed = st.checkbox(
                item["name"], 
                value=item["is_completed"], 
                key=f"check_{item['id']}"
            )
            
            # Als de status verandert in Supabase updaten
            if is_completed != item["is_completed"]:
                supabase.table("shopping_items").update({"is_completed": is_completed}).eq("id", item["id"]).execute()
                st.rerun()
                
        with col_del:
            # Direct verwijderen zonder melding (prullenbak icoon)
            if st.button("🗑️", key=f"del_{item['id']}"):
                supabase.table("shopping_items").delete().eq("id", item["id"]).execute()
                st.rerun()
