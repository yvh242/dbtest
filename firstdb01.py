import streamlit as st
from supabase import create_client

# 1. Verbinding maken
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    url = url.rstrip('/')
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_connection()

# 2. Simpele UI voor gebruiker toevoegen
st.title("Gebruikersregistratie")

naam = st.text_input("Naam")
email = st.text_input("Email")

if st.button("Opslaan"):
    # Data naar Supabase sturen
    data = supabase.table("gebruikers").insert({"naam": naam, "email": email}).execute()
    st.success("Gebruiker opgeslagen!")

# 3. Data tonen
st.subheader("Bestaande gebruikers")
st.title("Debug Scherm")
try:
    # Probeer de data op te halen en vang eventuele fouten af
    response = supabase.table("gebruikers").select("*").execute()
    st.success("Verbinding gelukt!")
    st.write(response.data)

except Exception as e:
    # Dit toont de exacte foutmelding die Supabase terugstuurt
    st.error(f"Volledige foutmelding: {e}")

