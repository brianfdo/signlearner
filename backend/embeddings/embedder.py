from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache

# Load a pre-trained sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

@lru_cache(maxsize=1000)
def get_embedding(text: str) -> np.ndarray:
    """
    Returns a dense vector embedding for the given text.
    Cached for performance optimization.
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding
