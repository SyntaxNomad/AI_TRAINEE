# ai_engine.py
import os
import csv
import io
from groq import Groq
import dotenv

dotenv.load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

BOUNDARY_MSG = "this question is not within the boundaries of this data"
CSV_DATA = "ucl-finals.csv"  

def load_csv_text(csv_bytes: bytes):
    """Load CSV into a single text block."""
    global CSV_DATA
    text = csv_bytes.decode("utf-8", "ignore")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    headers = rows[0]
    data_lines = [" | ".join(row) for row in rows[1:]]
    CSV_DATA = "\n".join([", ".join(headers)] + data_lines)

def answer_question(question: str) -> str:
    """Send the whole CSV to Groq and get an answer."""
    if not CSV_DATA.strip():
        return BOUNDARY_MSG

    messages = [
        {"role": "system", "content": f"Answer ONLY using the provided data. , give an answer if the question has anything related to the data. If the answer is not related to the data,  reply exactly: {BOUNDARY_MSG} be flexible and answer any question after going through the data to make sure the answer is suitable "},
        {"role": "user", "content": f"DATA:\n{CSV_DATA}\n\nQUESTION:\n{question}"}
    ]

    resp = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    return resp.choices[0].message.content.strip()