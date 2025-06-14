from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

#GROUP = "azubi"


#faiss_path = f"faiss_index/{group}_index"



PROMPT_TEMPLATES = {
    "azubi": """
Wichtig:
- Du darfst nur Fragen beantworten, für die es in den geladenen Frage-Antwort-Paaren eine passende Antwort gibt.
- Wenn die Frage nicht in diesen QA-Paaren enthalten ist, antworte ausschließlich:
  „Entschuldigung, dazu habe ich keine Information. Bitte frage in der internen Wissensbasis oder bei deinem Ansprechpartner nach.“

Du bist ein interner FAQ-Chatbot für Auszubildende in einem Unternehmen.
Deine Aufgabe ist es, auf Basis des Kontexts kurze, klare und verständliche Antworten zu geben.
Sprich auf Augenhöhe mit Auszubildenden (1.-3. Lehrjahr). Vermeide Fachjargon und bleib freundlich.

Falls die Information nicht eindeutig im Kontext steht, sage stattdessen:
„Diese Information liegt mir nicht eindeutig vor, frage bitte dein/e Ausbildungsleiter/in. Falls du nicht weißt, wer das ist, frag gerne hier im Chat nach.“

Kontext:
{context}

---

Frage:
{question}
""",

    "student": """
Du bist ein interner FAQ-Chatbot für dual Studierende im Unternehmen.
Antworte präzise, verständlich und studiennah. Beziehe dich nur auf den Kontext.

Falls etwas unklar ist, sag bitte:
„Diese Information liegt mir nicht eindeutig vor. Bitte frag deine:n Ausbilder:in oder Studienbetreuer:in.“

Kontext:
{context}

---

Frage:
{question}
"""
}
#Falls mehrere Optionen möglich sind, gib maximal zwei Alternativen an.                         | prompt zu template hinzufügen, falls output zu lang 

def run_query(query_text, group="azubi"):

#def run_query(query_text): # ohne gruppen abfrage |one dimensuionmal 

    embedding_function = OpenAIEmbeddings()

    faiss_path = f"faiss_index/{group}_index"
    db = FAISS.load_local(faiss_path, embedding_function, allow_dangerous_deserialization=True)

         # more dimensional

    #embedding_function = OpenAIEmbeddings()
    #db = FAISS.load_local(FAISS_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)                    |one dimensional


    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if not results or results[0][1] < 0.7:                                                                      #0.3 gibt mehr antworten zurück, 0.5 weniger
                                                                                                         #problem: gibt auf niedrige konfidenze lose antworten, also hallizuniert in dem sinne 
                                                                                                         # 0.3für testzwecke 
                                                                                                         # 0.7 nach vollständiger fragen katalog von isab. , dann greift auch 
                                                                                                         # höherer score alle fragen ab     
        return "KEINE PASSENDEN ERGEBNISSE GEFUNDEN. Bitte versuche es mit einer anderen Frage."

    context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATES[group])                 # more dimensional 
    prompt = prompt_template.format(context=context, question=query_text)


    #prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(context=context, question=query_text)    | one dimesnional 



#FALLBACK MODEL | WIRD AUTOMATISCH AUSGEWÄHLT WENN KEIN MODELL IN DER ENV HINTERLEGT IST 

    selected_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo")                    #wenn in der env kein modell hinterlegt ist, wird auf 3.5 turbo zurückgegriffen (automatisch)



    model = ChatOpenAI(model=selected_model, temperature=0)
# Je niedriger der Wert, desto konstanter ist die antwort (straight up antwort, kein drumherum reden)
# 0 = immer gleiche und faktisch klare antworten.
# hohe Werte wie 0.7 oder 1.0 führen zu mehr kreativität ( übermässige textgenerierung, halluzinationen)
# und ungenauigkeiten!!!
# In diesem Fall bewusst auf 0 gesetzt, damit bei gleichen Fragen auch gleiche antworten kommen 




    response = model.predict(prompt)

    return response

__all__ = ["run_query"]

