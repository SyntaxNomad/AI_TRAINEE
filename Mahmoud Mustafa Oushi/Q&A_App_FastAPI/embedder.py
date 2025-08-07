from sentence_transformers import SentenceTransformer
from file_parser import parse_file
from vector_store import VectorStoreSQLite
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
store = VectorStoreSQLite()

def embed_and_store(filename: str, content: bytes):
    text = parse_file(filename, content)

    # Chunk text in 500-char pieces
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    
    # Filter out empty or whitespace-only chunks
    filtered_chunks = [chunk for chunk in chunks if chunk.strip()]
    if len(filtered_chunks) < len(chunks):
        print(f"Filtered out {len(chunks) - len(filtered_chunks)} empty or whitespace-only chunks.")

    # Embed filtered chunks
    embeddings = model.encode(filtered_chunks).tolist()

    stored_chunks = []
    for chunk, embedding in zip(filtered_chunks, embeddings):
        # Check for NaN values in embedding vector
        if np.isnan(embedding).any():
            print(f"Warning: embedding contains NaN, skipping chunk: {chunk[:30]}...")
            continue
        store.add_chunk(filename, chunk, embedding)
        stored_chunks.append(chunk)
    
    return stored_chunks
