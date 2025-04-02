from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

FAISS_PATH = "faiss_index"
PROMPT_TEMPLATE = """
Beantworte die Nutzerfrage möglichst genau anhand des folgenden Kontexts.
Falls die Information nicht eindeutig im Kontext steht, gib eine fundierte Schätzung oder sage: "Diese Information liegt mir nicht eindeutig vor."

Kontext:
{context}

---

Frage: {question}
"""


def run_query(query_text):

    embedding_function = OpenAIEmbeddings()
    db = FAISS.load_local(FAISS_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    if not results or results[0][1] < 0.2:                                          
        return "KEINE PASSENDEN ERGEBNISSE GEFUNDEN. Bitte versuchen Sie es mit einer anderen Frage."

    context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(context=context, question=query_text)

    selected_model = os.getenv("GPT_MODEL", "gpt-3.5-turbo")
    model = ChatOpenAI(model=selected_model, temperature=0)
    response = model.predict(prompt)

    return response

__all__ = ["run_query"]

