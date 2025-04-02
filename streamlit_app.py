import streamlit as st
from query_data import run_query

import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="RAG FAQ-Tool", layout="centered")
st.title(" FAQ-Tool (RAG)")

st.markdown("Gib eine Frage ein, die auf unserer Knowledge Base basiert:")

user_input = st.text_input("Frage:")

if user_input:
    try:
        response = run_query(user_input)
        st.success(f"**Antwort:**\n\n{response}")
    except Exception as e:
        st.error(f"Es ist ein Fehler aufgetreten:\n\n{e}")
