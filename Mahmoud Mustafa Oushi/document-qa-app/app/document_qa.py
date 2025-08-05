import numpy as np
from app.config import Config
from app.embeddings import EmbeddingModel
from app.file_handler import FileHandler
from app.vector_index import VectorIndex
from app.llm_client import LLMClient

class DocumentQA:
    def __init__(self):
        self.embedder = EmbeddingModel(Config.EMBEDDING_MODEL)
        self.file_handler = FileHandler()
        self.llm = LLMClient(Config.GROQ_API_KEY)
        self.index = None
        self.chunks = []
        self.metadata = []

    def load_file(self, content: bytes, filename: str):
        self.file_handler.validate_file(filename)
        raw_data = self.file_handler.extract_text(content)
        self.metadata = self.file_handler.metadata

        chunks = raw_data if isinstance(raw_data, list) else self.file_handler.chunk_text(raw_data)
        self.chunks = chunks

        vectors = self.embedder.encode(chunks)
        self.index = VectorIndex(vectors.shape[1])
        self.index.add(vectors)

    def retrieve_chunks(self, query: str, k=10):
        query_vec = self.embedder.encode([query])
        D, I = self.index.search(query_vec, top_k=min(k, len(self.chunks)))
        return [(self.chunks[i], 1 - D[0][j], self.metadata[i] if self.metadata else {})
                for j, i in enumerate(I[0])]

    def ask(self, question: str, model: str = Config.DEFAULT_MODEL):
        context = self.retrieve_chunks(question)
        prompt = (
            f"Document: {self.file_handler.filename}\n"
            f"Relevant context:\n" + "\n\n".join(
                f"[Chunk {i+1}]\n{chunk[:500]}{'...' if len(chunk) > 500 else ''}"
                for i, (chunk, _, _) in enumerate(context)
            ) + f"\n\nQuestion: {question}\nAnswer concisely."
        )
        return self.llm.query(prompt, model)
