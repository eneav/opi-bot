import streamlit as st
from query_data import run_query
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="RAG FAQ-Tool", layout="centered")
st.title("FAQ-Tool für Auszubildende und (Dual)-Studierende")
st.write("Dieses Tool ermöglicht es dir, Fragen zu stellen und Antworten aus einer internen Knowledge Base zu erhalten.")


st.write("""
Bitte gib das Passwort deiner jeweiligen Abteilung ein. Diesen bekommst du von deinem Abteilungsleiter, deiner/m Ausbilder/in oder deinem Buddy:

- azubi = azubi123  
- student = student456
""")




password = st.text_input("Passwort:", type="password")

# mapping tabelle für die gruppen |

# anpassen mit neuer zugewisener datenbank mit eigenem index 
# neuer prompte template 
access_mapping = {
    "azubi123": "azubi",
    "student456": "student",
    "admin789": "admin"
}

if password:
    group = access_mapping.get(password.strip().lower()) #gruppen prüfeung, ob das passwort in der mapping tablle ist 


    if not group:
        st.error(" Falsches Passwort ")
    else:
        user_input = st.text_input("Frage:")
        if user_input:
            try:
                response = run_query(user_input, group=group)
                st.success(f"**Antwort ({group}):**\n\n{response}")
            except Exception as e:
                st.error(f"Es ist ein Fehler aufgetreten:\n\n{e}")
