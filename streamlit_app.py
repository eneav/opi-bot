import streamlit as st
from query_data import run_query
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="RAG FAQ-Tool", layout="centered")
st.title(" FAQ-Tool für Auszubildende und Studierende")
st.write("Dieses Tool ermöglicht es dir, Fragen zu stellen und Antworten aus einer internen Knowledge Base zu erhalten")  


st.markdown("Gib eine Frage ein, basierend auf der internen Knowledge Base:")

#  Gruppenauswahl (z. B. Azubi oder Student)
group = st.selectbox("Zielgruppe:", options=["azubi", "student"], index=0)

# Eingabefeld für Frage
user_input = st.text_input("Frage:")

if user_input:
    try:
        # Übergib die Gruppe an run_query
        response = run_query(user_input, group=group)
        st.success(f"**Antwort:**\n\n{response}")
    except Exception as e:
        st.error(f"Es ist ein Fehler aufgetreten:\n\n{e}")
