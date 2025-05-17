import os, json, base64
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from query_data import run_query
from utils.qa_validator import check_qa_pair  

#SETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUPSETUP
load_dotenv()
st.set_page_config(
    page_title="opi - CHATBOT",
    page_icon="img/opiicon.png",
    layout="centered",
)


def load_image_as_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


IMG_B64 = load_image_as_base64("img/opi.png")

#session state defaults (unfinished) 
for k, v in {
    "qa_pairs": [],
    "validation": [],
    "event_name": "",
    "current_question": "",
    "current_answer": "",
}.items():
    st.session_state.setdefault(k, v)

#sidebar
with st.sidebar:
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <img src="data:image/png;base64,{IMG_B64}" width="100">
            <h4 style='margin:12px 0 4px;'>opi-CHATBOT</h4>
            <p style='font-size:12px;color:gray;'>FAQ-Helfer für Azubis&nbsp;&amp;&nbsp;Studierende</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.subheader("Zugangscodes")
    st.markdown("azubi =`azubi123`  \nstudent = `student456`  \nadmin = `admin789`")
    st.markdown("---")
    if st.button("Zur Anleitung"):
        st.info("Die Anleitung findest du im Menüpunkt **README** im [GitHub-Repo](https://github.com/eneav/opi-bot).")

#titelblockj
st.markdown(
    f"""
    <div style='text-align:center;margin-top:15px;'>
        <img src="data:image/png;base64,{IMG_B64}" width="240">
    </div>
    <h1 style='text-align:center;margin-bottom:5px;'>opi - Interner Wissensassistent</h1>
    <hr style='width:300px;margin:auto;margin-bottom:25px;'>
    <p style='text-align:center;color:gray;margin-top:-10px;font-size:14px;'>
        Interner Assistenz-Chat für Wissensfragen
    </p>
    <p style='text-align:center;margin-top:-10px;margin-bottom:30px;font-size:13px;'>
        Bitte gib das Passwort deiner jeweiligen Abteilung ein. Diesen bekommst du von deinem Abteilungsleiter:
    </p>
    """,
    unsafe_allow_html=True,
)








#access_mapping passwort eingabeb 
password = st.text_input("Passwort:", type="password")
access_mapping = {"azubi123": "azubi", "student456": "student", "admin789": "admin"}
role = access_mapping.get(password.strip().lower()) if password else None




# if role == "admin":
#     st.subheader("Event-Editor (Admin)")


#     st.write("")  
#     st.markdown("---")
#     st.expander("", expanded=False) 

#     import json
#     from io import BytesIO


#     template_count = st.number_input(
#         "Vorlage: N leere QA-Paare erstellen", 
#         min_value=1, max_value=50, value=10, step=1,
#         help="Anzahl an leeren Frage/Antwort-Slots"
    
#     )
#     if st.button(" Leeres Template herunterladen"):
#         template = {
#             "event": "",
#             "qa_pairs": [{"Fragen": "", "Antworten": ""} for _ in range(template_count)]
#         }

#         bts = json.dumps(template, ensure_ascii=False, indent=2).encode("utf-8")
#         st.download_button(
#             "Download Template",
#             data=BytesIO(bts),
#             file_name=f"template_{template_count}_qa_pairs.json",
#             mime="application/json",
#         )


#     st.write("")  
#     st.markdown("---")
#     st.expander("", expanded=False) 




#     up = st.file_uploader("JSON-Datei importieren", type="json, key="uploader")
#     if up:
#         try:
#             data = json.load(up)
#             st.session_state.qa_pairs = data.get("qa_pairs", [])
#             st.session_state.event_name = data.get("event", "Importiertes Event")
#             st.success(f"{len(st.session_state.qa_pairs)} Paare importiert.")
#         except Exception as e:
#             st.error(f"Fehler beim Laden: {e}")
#     st.write("")  
#     st.markdown("---")
#     st.expander("", expanded=False)  # nur für Abstand, ohne Inhalt




if role == "admin":
    st.subheader("Event-Editor (Admin)")

    # 🔹 dezenter Divider oben
    st.markdown("<hr style='margin-top:4px;'>", unsafe_allow_html=True)



#TEMPLATE GENERATOR  

    st.number_input(
        "Leere QA-Paare generieren (Anzahl)",
        min_value=1, max_value=50, value=10, step=1,
        key="tpl_rows",
        help="Wie viele leere Zeilen soll das json Template enthalten?"
    )

    if st.button("Leeres Template herunterladen"):
        empty_tpl = {
            "event": "",
            "qa_pairs": [{"Fragen": "", "Antworten": ""}] * st.session_state.tpl_rows,
        }
        st.download_button(
            "JSON laden",
            data=json.dumps(empty_tpl, ensure_ascii=False, indent=2).encode("utf-8"),
            file_name="leeres_template.json",
            mime="application/json",
        )


    st.markdown("___", unsafe_allow_html=True)




#json import // mehh.. unfinished. session state macht probleme 
#import + manuelle eingabe kollidieren.

#nur import und dessen bearbeitung funktioniert 
#nur manuelle eingabe und deren bearbeitung funktioniert


    up = st.file_uploader("JSON-Datei importieren", type="json", key="uploader")
    if up:
        try:
            data = json.load(up)
            st.session_state.qa_pairs = data.get("qa_pairs", [])
            st.session_state.event_name = data.get("event", "Importiertes Event")
            st.success(f"{len(st.session_state.qa_pairs)} Paare importiert.")
        except Exception as e:
            st.error(f"Fehler beim Laden: {e}")

    # 🔹 noch einmal Luft, bevor der Name & Tabelle kommen
    st.markdown("<hr>", unsafe_allow_html=True)

    st.text_input("Event-Name:", key="event_name")                                         #event name eingabe
                                                                                          #ohne event name, einfache installation von 
                                                                                           #einer json. || gotta fix that 
     

#data editor tabelle 

#selbst keine ahnung was hier passiert, aber es funktioniert
    base_df = pd.DataFrame(
        st.session_state.qa_pairs or [{"Fragen": "", "Antworten": ""}]
    )


#doku: 
# https://docs.streamlit.io/develop/api-reference/data/st.dataframe


    # Nummerierung IMMMMERRR neu berechnen
    base_df = base_df.reset_index(drop=True)  
    base_df.insert(0, "#", base_df.index + 1) 

    edited_df = st.data_editor(
        base_df,
        num_rows="dynamic",  
        hide_index=True, 
        use_container_width=True,
        key="qa_editor",
    )

    cleaned = (
        edited_df.dropna(subset=["Fragen", "Antworten"]) 
        .query("Fragen != '' and Antworten != ''")
        .drop(columns=["#"])
        .to_dict(orient="records")
    )
    if st.button("Änderungen übernehmen und speichern"):
        st.session_state.qa_pairs = cleaned
        st.success(f"{len(cleaned)} Paare gespeichert.")



        
#++++++++


#validierung der llm analyse 
#/muss noch cursor an button hinzufügen, damit user weiss das analyse läuft aktuell 
    if st.button("Inhalt prüfen"):
        with st.spinner("LLM prüft Inhalte..."):    #läuft mit der abluf der analyse. node wird getriggert 
            problems = []
            for i, p in enumerate(st.session_state.qa_pairs, 1):
                res = check_qa_pair(p["Fragen"], p["Antworten"])
                if res["status"] != "ok":
                    problems.append((i, res["status"], res["feedback"]))
            st.session_state.validation = problems

        if not problems: #ergebnis  validierung
            st.success("Alle QA-Paare sehen gut aus.")
        else:
            colors = {"warn": "orange", "error": "red"}
            for i, status, fb in problems:
                st.markdown(
                    f"<span style='color:{colors[status]}'>#{i} – {fb}</span>",
                    unsafe_allow_html=True,
                )
            st.warning("Bitte überarbeite die markierten Einträge und prüfe erneut.")

#+++++++++++++++










    if st.session_state.qa_pairs:
        json_bytes = json.dumps(
            {"event": st.session_state.event_name, "qa_pairs": st.session_state.qa_pairs},
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8")
        st.download_button(
            "JSON-Datei herunterladen",
            data=json_bytes,
            file_name=f"{st.session_state.event_name.lower().replace(' ', '_')}.json",
            mime="application/json",
        )











#AB HIER AB HIER AB HIER 
#alles ausser admin 
#faq beriech wie gehabt aus version .0.0.1




elif role in {"azubi", "student"}:
    question = st.text_input("Frage:")
    if question:
        try:
            answer = run_query(question, group=role)
            st.success(answer)
        except Exception as e:
            st.error(f"Fehler: {e}")


elif password:
    st.error("Falsches Passwort - bitte prüfe deine Eingabe.")


st.markdown(
    "<p style='text-align:center;font-size:12px;color:gray;'>"
    "Mehr Infos auf <a href='https://github.com/eneav/opi-bot' target='_blank'>GitHub</a>"
    "</p>",
    unsafe_allow_html=True,
)
