import os, io, re, json, pandas as pd, PyPDF2
from app.config import Config

class FileHandler:
    def __init__(self):
        self.filename = ""
        self.metadata = []

    def validate_file(self, filename):
        ext = os.path.splitext(filename.lower())[1]
        if ext not in Config.SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {ext}")
        self.filename = filename

    def extract_text(self, uploaded_bytes: bytes):
        if self.filename.endswith('.pdf'):
            return self._extract_pdf(uploaded_bytes)
        elif self.filename.endswith('.json'):
            return self._extract_json(uploaded_bytes)
        elif self.filename.endswith('.csv'):
            return self._extract_csv(uploaded_bytes)
        elif self.filename.endswith('.txt'):
            return uploaded_bytes.decode('utf-8')

    def _extract_pdf(self, content):
        reader = PyPDF2.PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() or f"[Page {i+1}] Empty" for i, page in enumerate(reader.pages))

    def _extract_json(self, content):
        data = json.loads(content.decode('utf-8'))
        return json.dumps(data, indent=2) if isinstance(data, dict) else "\n".join(json.dumps(d, indent=2) for d in data)

    def _extract_csv(self, content):
        df = pd.read_csv(io.BytesIO(content))
        rows = []
        for _, row in df.iterrows():
            rows.append("\n".join(f"{col}: {row[col]}" for col in df.columns))
        self.metadata = [{"chunk_id": i, "content_type": "csv_row", "source": self.filename} for i in range(len(rows))]
        return rows

    def chunk_text(self, text):
        text = re.sub(r'\s+', ' ', text).strip().replace("-\n", "")
        words = text.split()
        return [
            ' '.join(words[i:i + Config.CHUNK_SIZE])
            for i in range(0, len(words), Config.CHUNK_SIZE - Config.CHUNK_OVERLAP)
        ]
