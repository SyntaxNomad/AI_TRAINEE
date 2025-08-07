from vector_store_sqlite import VectorStoreSQLite

db = VectorStoreSQLite()

chunks = db.get_all_chunks()

for chunk in chunks:
    print(f"ID: {chunk.id}")
    print(f"Filename: {chunk.filename}")
    print(f"Text: {chunk.text[:100]}...")  
    print(f"Embedding: {chunk.embedding[:60]}...")  
    print("-" * 40)
