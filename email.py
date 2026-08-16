import urllib.parse
import streamlit as st

st.set_page_config(page_title="Outlook E-mail Generator", page_icon="📧", layout="centered")

st.title("📧 Outlook E-mail Generator")
st.write(
    "Vul de gegevens hieronder in om een kant-en-klare e-mail klaar te zetten in Outlook."
)

# Formulier voor de e-mailgegevens
with st.form("email_form"):
    to_email = st.text_input(
        "Ontvanger (E-mailadres)", placeholder="naam@voorbeeld.be"
    )
    subject = st.text_input("Onderwerp", placeholder="Bijv. Status update zending")
    body = st.text_area(
        "Bericht",
        placeholder="Typ hier je bericht...",
        height=150,
    )

    submitted = st.form_submit_button("E-mail klaarzetten in Outlook")

if submitted:
    if not to_email:
        st.warning("Gelieve ten minste een e-mailadres van de ontvanger in te vullen.")
    else:
        # Url encode de tekst zodat spaties en speciale tekens correct meegaan
        encoded_subject = urllib.parse.quote(subject)
        encoded_body = urllib.parse.quote(body)

        # Maak de mailto link
        mailto_link = (
            f"mailto:{to_email}?subject={encoded_subject}&body={encoded_body}"
        )

        # Toon een knop met een HTML-link die de mailto opent
        st.success("Je e-mail is klaar!")
        st.markdown(
            f"""
            <a href="{mailto_link}" target="_blank">
                <button style="
                    background-color: #0078D4; 
                    color: white; 
                    padding: 10px 20px; 
                    border: none; 
                    border-radius: 4px; 
                    font-size: 16px; 
                    cursor: pointer;
                    font-weight: bold;">
                    Open in Outlook / E-mailclient 🚀
                </button>
            </a>
            """,
            unsafe_allow_html=True,
        )
        st.info(
            "Als Outlook niet automatisch opent, klik dan op de blauwe knop hierboven."
        )
