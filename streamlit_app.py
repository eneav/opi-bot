import streamlit as st
from query_data import run_query
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="opi - CHATBOT",
    page_icon="img/opiicon.png",  
    layout="centered"
)


# st.markdown(
#     """
#     <div style='text-align: center;'>
#         <img src='./img/opi.png' width='80'/>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

import base64

def load_image_as_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = load_image_as_base64("img/opi.png")
st.markdown(
    f"""
    <div style='text-align: center; margin-top: -20px; margin-bottom: 30px;'>
        <img src="data:image/png;base64,{img_base64}" width="240"/>
    </div>
    """,
    unsafe_allow_html=True
)




with st.sidebar:
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 20px; margin-bottom: 15px;'>
            <img src="data:image/png;base64,{img_base64}" width="100"/>
            <h4 style='margin-top: 12px; margin-bottom: 4px;'>opi-CHATBOT</h4>
            <p style='font-size: 12px; color: gray;'>Dein FAQ-Helfer für Azubis & Studierende</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.subheader("Zugangscodes")
    st.markdown(" **azubi** = `azubi123`  \n **student** = `student456`")
    st.markdown("---")

    st.markdown("---")
    st.markdown("Wähle deine Gruppe aus")

    if st.button("Zur Anleitung"):
        st.info("Die Anleitung findest du im Menüpunkt [README auf GitHub](https://github.com/eneav/opi-bot.git).")








# st.title("FAQ-Tool für Auszubildende und (Dual)-Studierende")
# st.write("Dieses Tool ermöglicht es dir, Fragen zu stellen und Antworten aus einer internen Knowledge Base zu erhalten.")
# st.title("FAQ-Tool für Auszubildende und (Dual)-Studierende")
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 5px;'>opi – Interner Wissensassistent</h1>
    <hr style='width: 300px; margin: auto; margin-bottom: 30px;'/>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; margin-top: -15px; margin-bottom: 30px; color: gray; font-size: 16px;'>Interner Assistenz-Chat für Wissensfragen</p>",
    unsafe_allow_html=True
)






# st.write("""
# Bitte gib das Passwort deiner jeweiligen Abteilung ein. Diesen bekommst du von deinem Abteilungsleiter, deiner/m Ausbilder/in oder deinem Buddy:

# - azubi = azubi123  
# - student = student456
# """)




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
