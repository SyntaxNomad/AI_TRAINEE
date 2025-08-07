import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPPORTED_FILE_TYPES = {'.pdf', '.csv', '.json', '.txt'}
    DEFAULT_MODEL = "llama3-8b-8192"
    MAX_CONTEXT_LENGTH = 24000
    CHUNK_SIZE = 4096
    CHUNK_OVERLAP = 50
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
