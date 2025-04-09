from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

FAISS_PATH = "faiss_index"
PROMPT_TEMPLATE = """
Du bist ein interner FAQ-Chatbot für Auszubildende in einem Unternehmen.
Deine Aufgabe ist es, auf Basis des Kontexts kurze, klare und verständliche Antworten zu geben. 
Sprich auf Augenhöhe mit Auszubildenden (1.-3. Lehrjahr). Vermeide Fachjargon und bleib freundlich.

Falls die Information nicht eindeutig im Kontext steht, sage stattdessen:
„Diese Information liegt mir nicht eindeutig vor, frage bitte dein/e Ausbildungsleiter/in“ 

Kontext:
{context}

---

Frage:
{question}
"""


def run_query(query_text):

    embedding_function = OpenAIEmbeddings()
    db = FAISS.load_local(FAISS_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if not results or results[0][1] < 0.5:                                          
        return "KEINE PASSENDEN ERGEBNISSE GEFUNDEN. Bitte versuche es mit einer anderen Frage."

    context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(context=context, question=query_text)



    selected_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo")

    
    model = ChatOpenAI(model=selected_model, temperature=0)


    response = model.predict(prompt)

    return response

__all__ = ["run_query"]

