from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

class PathwayStore:
    def __init__(self, chunks: List[str]):
        """Simple in-memory store with precomputed embeddings.

        chunks: List[str]
        """
        self.chunks = chunks
        self.embeddings = self._embed_chunks(chunks)

    def _embed_chunks(self, chunks: List[str]) -> np.ndarray:
        if not chunks:
            dim = model.get_sentence_embedding_dimension()
            return np.empty((0, dim), dtype=np.float32)
        return model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.chunks:
            return []
        q = model.encode(query, convert_to_numpy=True, normalize_embeddings=True)
        scores = self.embeddings @ q
        k = min(top_k, len(self.chunks))
        top_indices = np.argsort(-scores)[:k]
        return [self.chunks[i] for i in top_indices]
