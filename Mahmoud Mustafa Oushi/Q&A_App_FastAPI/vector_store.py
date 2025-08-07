from sentence_transformers import SentenceTransformer
from vector_store_sqlite import VectorStoreSQLite  

model = SentenceTransformer("all-MiniLM-L6-v2")
store = VectorStoreSQLite()

def retrieve_similar_chunks(query: str, top_k: int = 5):
    embedding = model.encode(query).tolist()
    similar = store.search_similar_chunks(embedding, top_k=top_k)
    return [chunk for score, chunk in similar]


