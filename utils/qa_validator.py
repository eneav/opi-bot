import os, json, textwrap
from openai import OpenAI

client = OpenAI()
MODEL = os.getenv("GPT_MODEL_VALIDATOR", "gpt-4-0125-preview")

def check_qa_pair(question: str, answer: str) -> dict:
    prompt = textwrap.dedent(f"""
    Prüfe Frage + Antwort auf
    - Verständlichkeit
    - Korrektheit
    - Dopplung/Wiederholung

    Antworte **streng** im JSON-Format:
    {{
    "status": "ok|warn|error",
    "feedback": "<ein kurzer Satz>"
    }}

    Frage: "{question}"
    Antwort: "{answer}"
    """).strip()



    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,          # minimal Kreativität für den Hint
    )

    return json.loads(resp.choices[0].message.content)
