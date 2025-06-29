import chromadb
from chromadb.config import Settings
import numpy as np

# Initialize Chroma client
client = chromadb.Client(Settings(
    persist_directory="chroma_db"
))

# Create a collection (if it doesn't exist)
collection_name = "asl_videos"
collection = client.get_or_create_collection(name=collection_name)

def add_video_to_db(video_id: str, title: str, embedding: np.ndarray, metadata: dict):
    """
    Adds a video to the vector database.
    """
    collection.add(
        ids=[video_id],
        embeddings=[embedding.tolist()],
        documents=[title],
        metadatas=[metadata]
    )

def query_similar_videos(query_embedding: np.ndarray, top_k=5):
    """
    Queries the vector DB for videos similar to the provided embedding.
    """
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["distances", "metadatas", "documents"]
    )
    return results
