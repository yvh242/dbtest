import streamlit as st

# Pagina instellingen
st.set_page_config(page_title="Fleet Dispatch - Mock Versie", layout="wide")

st.title("🚛 Nationale Dispatch - Oplegger & Chauffeur Beheer (Mock)")
st.markdown("Beheer hier lokaal de vloot, wijzig statuten en koppel chauffeurs aan opleggers.")

# --- 1. INITIALISATIE VAN LOKALE DATA (SESSION STATE) ---
if 'chauffeurs' not in st.session_state:
    st.session_state.chauffeurs = [
        {"id": 1, "naam": "Jan Peeters"},
        {"id": 2, "naam": "Marc Dubois"},
        {"id": 3, "naam": "Luc de Smet"},
        {"id": 4, "naam": "Tom Vermeulen"}
    ]

if 'opleggers' not in st.session_state:
    st.session_state.opleggers = [
        {"id": 1, "code": "OPL-101", "status": "vrij", "chauffeur": None},
        {"id": 2, "code": "OPL-102", "status": "in gebruik", "chauffeur": "Jan Peeters"},
        {"id": 3, "code": "OPL-103", "status": "garage", "chauffeur": None},
        {"id": 4, "code": "OPL-104", "status": "vrij", "chauffeur": None},
        {"id": 5, "code": "OPL-105", "status": "vrij", "chauffeur": None}
    ]

# --- 2. ZIJBALK: SNEL EXTRA DATA TOEVOEGEN ---
with st.sidebar:
    st.header("➕ Extra Item Toevoegen")
    
    # Nieuwe chauffeur
    new_ch = st.text_input("Naam nieuwe chauffeur")
    if st.button("Voeg chauffeur toe"):
        if new_ch:
            new_id = max([c['id'] for c in st.session_state.chauffeurs], default=0) + 1
            st.session_state.chauffeurs.append({"id": new_id, "naam": new_ch})
            st.success(f"Chauffeur {new_ch} toegevoegd!")
            st.rerun()
            
    st.divider()
    
    # Nieuwe oplegger
    new_op = st.text_input("Code nieuwe oplegger (bijv. OPL-106)")
    if st.button("Voeg oplegger toe"):
        if new_op:
            st.session_state.opleggers.append({"id": len(st.session_state.opleggers) + 1, "code": new_op, "status": "vrij", "chauffeur": None})
            st.success(f"Oplegger {new_op} toegevoegd!")
            st.rerun()

# --- 3. HOOFDSCHERM: VISUEEL OVERZICHT & TOEWIZEN ---
col_overzicht, col_actie = st.columns([2, 1])

with col_overzicht:
    st.subheader("📋 Vloot Status Overzicht")
    
    # Filters voor status
    status_filter = st.radio("Filter op status:", ["Alle", "vrij", "in gebruik", "garage"], horizontal=True)
    
    for op in st.session_state.opleggers:
        if status_filter != "Alle" and op['status'] != status_filter:
            continue
            
        # Status styling badges
        status = op['status']
        if status == 'in gebruik':
            badge = "🔴 In gebruik"
        elif status == 'garage':
            badge = "🟡 Garage"
        else:
            badge = "🟢 Vrij"
            
        chauffeur_tekst = op['chauffeur'] if op['chauffeur'] else "Geen chauffeur toegewezen"
        
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 1.5, 1.5])
            c1.markdown(f"### **{op['code']}**")
            c2.markdown(f"**Status:** {badge}")
            c3.markdown(f"**Chauffeur:** {chauffeur_tekst}")

with col_actie:
    st.subheader("⚙️ Snelle Toewijzing")
    
    # Formulier om oplegger te koppelen
    oplegger_codes = [op['code'] for op in st.session_state.opleggers]
    gekozen_oplegger_code = st.selectbox("Selecteer Oplegger:", oplegger_codes)
    
    chauffeur_namen = [ch['naam'] for ch in st.session_state.chauffeurs]
    chauffeur_namen.insert(0, "-- Geen / Loskoppelen --")
    gekozen_chauffeur = st.selectbox("Selecteer Chauffeur:", chauffeur_namen)
    
    beschikbare_statussen = ["vrij", "in gebruik", "garage"]
    gekozen_status = st.selectbox("Nieuwe Status:", beschikbare_statussen)
    
    if st.button("Wijziging Doorvoeren", type="primary"):
        # Zoek de oplegger en update de data in session_state
        for op in st.session_state.opleggers:
            if op['code'] == gekozen_oplegger_code:
                op['status'] = gekozen_status
                if gekozen_chauffeur == "-- Geen / Loskoppelen --":
                    op['chauffeur'] = None
                    if gekozen_status == "in gebruik":
                        op['status'] = "vrij" # Kan niet 'in gebruik' zijn zonder chauffeur
                else:
                    op['chauffeur'] = gekozen_chauffeur
                    op['status'] = "in gebruik" # Automatisch naar in gebruik bij koppeling
                break
        
        st.success(f"Oplegger {gekozen_oplegger_code} succesvol bijgewerkt!")
        st.rerun()
