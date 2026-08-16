import streamlit as st

st.set_page_config(page_title="Fleet Dispatch - Dashboard", layout="wide")

st.title("🚛 Nationale Dispatch - Vloot & Chauffeurs Beheer")

# --- DATA INITIALISATIE ---
if 'chauffeurs' not in st.session_state:
    st.session_state.chauffeurs = [
        {"id": 1, "naam": "Jan Peeters", "oplegger": "OPL-102"},
        {"id": 2, "naam": "Marc Dubois", "oplegger": None},
        {"id": 3, "naam": "Luc de Smet", "oplegger": None},
        {"id": 4, "naam": "Tom Vermeulen", "oplegger": None}
    ]

if 'opleggers' not in st.session_state:
    st.session_state.opleggers = [
        {"id": 1, "code": "OPL-101", "status": "vrij"},
        {"id": 2, "code": "OPL-102", "status": "in gebruik"},
        {"id": 3, "code": "OPL-103", "status": "garage"},
        {"id": 4, "code": "OPL-104", "status": "vrij"},
        {"id": 5, "code": "OPL-105", "status": "vrij"}
    ]

# --- HOOFDSCHERM: TWEE KOLOMMEN (Naast elkaar i.p.v. tabs) ---
col_opleggers, col_chauffeurs = st.columns(2)

with col_opleggers:
    st.subheader("📦 Opleggers Vloot")
    
    for op in st.session_state.opleggers:
        # Zoek welke chauffeur deze oplegger heeft (indien van toepassing)
        toegewezen_aan = "Niemand"
        for ch in st.session_state.chauffeurs:
            if ch['oplegger'] == op['code']:
                toegewezen_aan = ch['naam']
                break
        
        # Status badge
        status = op['status']
        if status == 'in gebruik':
            badge = f"🔴 In gebruik ({toegewezen_aan})"
        elif status == 'garage':
            badge = "🟡 Garage"
        else:
            badge = "🟢 Vrij"
            
        with st.container(border=True):
            c1, c2 = st.columns([2, 3])
            c1.markdown(f"### **{op['code']}**")
            c2.markdown(f"**Status:** {badge}")
            
            # Snelle status knop om in/uit garage te zetten
            if status != 'in gebruik':
                nieuwe_status = "garage" if status == 'vrij' else "vrij"
                if st.button(f"Zet in {nieuwe_status}", key=f"status_{op['code']}"):
                    op['status'] = 'garage' if status == 'vrij' else 'vrij'
                    st.rerun()

with col_chauffeurs:
    st.subheader("👨‍✈️ Chauffeurs & Koppelingen")
    
    for ch in st.session_state.chauffeurs:
        huidige_opl = ch['oplegger'] if ch['oplegger'] else "Geen oplegger"
        
        with st.container(border=True):
            st.markdown(f"### **{ch['naam']}**")
            st.write(gekomen_tekst := f"Gekoppelde oplegger: **{huidige_opl}**")
            
            # Selectbox om direct een vrije oplegger te koppelen of los te koppelen
            vrije_opleggers = [o['code'] for o in st.session_state.opleggers if o['status'] == 'vrij' or o['code'] == ch['oplegger']]
            vrije_opleggers.insert(0, "-- Geen oplegger --")
            
            # Huidige index bepalen
            huidige_index = 0
            if ch['oplegger'] in vrije_opleggers:
                huidige_index = vrije_opleggers.index(ch['oplegger'])
                
            gekozen_op = st.selectbox(
                "Koppel oplegger:", 
                vrije_opleggers, 
                index=huidige_index, 
                key=f"select_{ch['id']}"
            )
            
            # Actie knop om wijziging door te voeren
            if st.button(f"Opslaan voor {ch['naam']}", key=f"btn_{ch['id']}"):
                oude_opl = ch['oplegger']
                
                if gekozen_op == "-- Geen oplegger --":
                    # Maak oude oplegger weer vrij
                    if oude_opl:
                        for o in st.session_state.opleggers:
                            if o['code'] == oude_opl:
                                o['status'] = 'vrij'
                    ch['oplegger'] = None
                else:
                    # Oude oplegger vrijmaken
                    if oude_opl and oude_opl != gekozen_op:
                        for o in st.session_state.opleggers:
                            if o['code'] == oude_opl:
                                o['status'] = 'vrij'
                    
                    # Nieuwe oplegger bezetten
                    ch['oplegger'] = gekozen_op
                    for o in st.session_state.opleggers:
                        if o['code'] == gekozen_op:
                            o['status'] = 'in gebruik'
                            
                st.success(f"Koppeling gewijzigd voor {ch['naam']}!")
                st.rerun()
