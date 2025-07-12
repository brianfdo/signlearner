import chromadb
import numpy as np

# Initialize Chroma client with persistence
client = chromadb.PersistentClient(
    path="chroma_db",  # simplified path configuration
)

# Create a collection (if it doesn't exist)
collection_name = "asl_videos"
collection = client.get_or_create_collection(name=collection_name)

def add_video_to_db(video_id, title, embedding, metadata):
    print(f"Adding video id={video_id}, title={title}")
    print(f"Embedding sample: {embedding[:5]}")  # print first 5 floats
    try:
        collection.add(
            ids=[video_id],
            embeddings=[embedding.tolist()],
            documents=[title],
            metadatas=[metadata]
        )
        print(f"Added successfully.")
    except Exception as e:
        print(f"Error adding video: {e}")
    print(f"Adding video id={video_id}, title={title}")

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

def list_all_videos():
    results = collection.get(include=["documents", "metadatas", "ids"])
    return results
