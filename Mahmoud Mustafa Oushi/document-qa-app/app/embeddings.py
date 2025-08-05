from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

class EmbeddingModel:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        vectors = self.model.encode(texts, convert_to_tensor=False)
        return normalize(vectors, axis=1, norm='l2')
