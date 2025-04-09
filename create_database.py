import os
import shutil
import pandas as pd
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
print("API-Key:", os.getenv("OPENAI_API_KEY"))


DATA_PATHS = [                          
    "data/sourcedata01_fixed.csv",
    "data/sourcedata01_questions_formulated.csv"
]

#DATA_PATH = "data/sourcedata01_fixed.csv"

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_faiss(chunks)

def load_documents():                                                                                 #function wurde angepasst damit sie mehr als nur eine csv datei laden kann
    all_rows = []                                                                                     #data path=paths mit for schelife fäntg sie alle datein im data/ ab 

    for path in DATA_PATHS:                                                                           #lädt alle csv datein im data/ ab | FÜR SKALIIERUNG EINGEBAUT 
        df = pd.read_csv(path)
        if "Fragen" not in df.columns or "Antworten" not in df.columns:
            raise ValueError(f"CSV '{path}' muss Spalten 'Fragen' und 'Antworten' enthalten")

        rows = [Document(page_content=row["Antworten"], metadata={"Frage": row["Fragen"]})
                for _, row in df.iterrows()]
        all_rows.extend(rows)

    return all_rows



#def load_documents():                                                                                      #function wurde angepasst damit sie mehr als nur eine csv datei laden kann
                                                                                                            #ursprünglich für NUR EINE csv date , bei rückker zeile 19 reaktivieren    
    df = pd.read_csv(DATA_PATH)
    if "Fragen" not in df.columns or "Antworten" not in df.columns:
        raise ValueError("CSV muss Spalten 'Fragen' und 'Antworten' enthalten")

    return [Document(page_content=row["Antworten"], metadata={"Frage": row["Fragen"]}) for _, row in df.iterrows()]


def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    return splitter.split_documents(documents)

from langchain_community.vectorstores import FAISS

def save_to_faiss(chunks):
    db = FAISS.from_documents(chunks, OpenAIEmbeddings())
    db.save_local("faiss_index")
    print(f"ERFOLGREICH {len(chunks)} Chunks in FAISS datenbank gespeichert.")



if __name__ == "__main__":
    generate_data_store()
    print("Datenbank erfolgreich erstellt!")

