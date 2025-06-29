from sentence_transformers import SentenceTransformer
import numpy as np

# Load a pre-trained sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
    """
    Returns a dense vector embedding for the given text.
    """
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding
