import fitz  
import pandas as pd
import json

def parse_pdf(content: bytes) -> str:
    doc = fitz.open("pdf", content)
    return "\n".join(page.get_text() for page in doc)

def parse_csv(content: bytes) -> str:
    df = pd.read_csv(pd.io.common.BytesIO(content))
    df = df.fillna('') 
    return df.to_string(index=False)  

def parse_txt(content: bytes) -> str:
    return content.decode("utf-8")

def parse_json(content: bytes) -> str:
    data = json.loads(content.decode("utf-8"))
    return json.dumps(data, indent=2)

def parse_file(filename: str, content: bytes) -> str:
    if filename.endswith(".pdf"):
        return parse_pdf(content)
    elif filename.endswith(".csv"):
        return parse_csv(content)
    elif filename.endswith(".txt"):
        return parse_txt(content)
    elif filename.endswith(".json"):
        return parse_json(content)
    else:
        raise ValueError("Unsupported file type")
