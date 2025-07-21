import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from embeddings.embedder import get_embedding
from api.vector_db_utils import add_video_to_db
from config import VECTOR_SEARCH_STOP_TOKEN

# Path to your scraped ASL video metadata
VIDEO_DATA_PATH = "asl_data/asl_videos.json"

def ingest_videos():
    with open(VIDEO_DATA_PATH, "r") as f:
        videos = json.load(f)

    for video in videos:
        video_id = video["videoId"]
        original_title = video["title"]
        
        # Create enhanced title for better vector search matching
        # This aligns with how users typically search by using consistent stop token
        enhanced_title = f"{original_title} {VECTOR_SEARCH_STOP_TOKEN}"
        
        # Use enhanced title for embedding to improve search similarity
        embedding = get_embedding(enhanced_title)

        metadata = {
            "url": video["url"],
            "duration": video["duration"],
            "original_title": original_title  # Preserve original for display if needed
        }

        # Store the enhanced title as the document for better search matching
        add_video_to_db(video_id, enhanced_title, embedding, metadata)
        print(f"✅ Ingested: {original_title} -> {enhanced_title}")

if __name__ == "__main__":
    print(f"🚀 Starting ingestion with stop token: '{VECTOR_SEARCH_STOP_TOKEN}'")
    ingest_videos()
    print("🎉 Ingestion complete. Enhanced titles for better search matching!")

