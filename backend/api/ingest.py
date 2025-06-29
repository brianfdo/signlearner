import json
from embeddings.embedder import get_embedding
from api.vector_db_utils import add_video_to_db

# Path to your scraped ASL video metadata
VIDEO_DATA_PATH = "asl_data/asl_videos.json"

def ingest_videos():
    with open(VIDEO_DATA_PATH, "r") as f:
        videos = json.load(f)

    for video in videos:
        video_id = video["videoId"]
        title = video["title"]
        embedding = get_embedding(title)

        metadata = {
            "url": video["url"],
            "duration": video["duration"]
        }

        add_video_to_db(video_id, title, embedding, metadata)
        print(f"✅ Ingested: {title}")

if __name__ == "__main__":
    ingest_videos()
    print("🎉 Ingestion complete. DB ready at chroma_db/")

