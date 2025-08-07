import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "PUT_KEY")
GROQ_API_URL = "PUT_URL"

def query(context: str, question: str):
    prompt = (
        "Use ONLY the following context to answer the question. "
        "If the answer is not in the context, reply 'I don't know.'\n\n"
        "Context:\n" + context + "\n\n"
        "Question:\n" + question
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"


