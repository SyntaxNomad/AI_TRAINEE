import faiss
import numpy as np

class VectorIndex:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)

    def add(self, vectors):
        self.index.add(vectors.astype(np.float32))

    def search(self, query_vector, top_k=10):
        D, I = self.index.search(query_vector.astype(np.float32), top_k)
        return D, I
