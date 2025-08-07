# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy import Column, Integer, String
# from pgvector.sqlalchemy import Vector
# import os
# from dotenv import load_dotenv
# from sqlalchemy import text
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# engine = create_engine(DATABASE_URL)

# with engine.connect() as conn:
#     conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


# SessionLocal = sessionmaker(bind=engine)
# Base = declarative_base()

# class DocumentChunk(Base):
#     __tablename__ = "document_chunks"

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, index=True)
#     text = Column(String)
#     embedding = Column(Vector(384)) 

# Base.metadata.create_all(bind=engine)

import os
import json
import numpy as np
from typing import List, Tuple
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = "sqlite:///./vectors.db"

Base = declarative_base()

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True)
    filename = Column(String, index=True)
    text = Column(Text)
    embedding = Column(Text)  

class VectorStoreSQLite:
    def __init__(self, db_url: str = DB_PATH):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_chunk(self, filename: str, text: str, embedding: List[float]):
        session = self.Session()
        chunk = DocumentChunk(
            filename=filename,
            text=text,
            embedding=json.dumps(embedding)
        )
        session.add(chunk)
        session.commit()
        session.close()

    def get_all_chunks(self) -> List[DocumentChunk]:
        session = self.Session()
        chunks = session.query(DocumentChunk).all()
        session.close()
        return chunks

    def search_similar_chunks(
        self,
        query_embedding: List[float],
        top_k: int = 5
    ) -> List[Tuple[float, DocumentChunk]]:
        session = self.Session()
        chunks = session.query(DocumentChunk).all()
        results = []
        query_vec = np.array(query_embedding)

        for chunk in chunks:
            stored_vec = np.array(json.loads(chunk.embedding))
            sim = float(np.dot(query_vec, stored_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(stored_vec)
            ))
            results.append((sim, chunk))

        session.close()
        # Sort by similarity descending
        return sorted(results, key=lambda x: x[0], reverse=True)[:top_k]
