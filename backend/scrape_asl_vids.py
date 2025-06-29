from googleapiclient.discovery import build
import isodate
import json
import config

API_KEY = config.API_KEY       
CHANNEL_ID = "UCZy9xs6Tn9vWqN_5l0EEIZA"  # ASLU official channel ID

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_playlists(channel_id):
    playlists = []
    request = youtube.playlists().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50
    )
    response = request.execute()
    print(f"Found {len(response.get('items', []))} playlists for channel {channel_id}")
    for item in response.get("items", []):
        title = item["snippet"]["title"]
        # Filter to only ASLU Lesson Review Playlists by name
        if "aslu lesson" in title.lower():
            playlists.append({
                "id": item["id"],
                "title": title
            })
    return playlists

def get_videos_from_playlist(playlist_id):
    videos = []
    nextPageToken = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response.get("items", []):
            videos.append(item["contentDetails"]["videoId"])
        nextPageToken = response.get("nextPageToken")
        if not nextPageToken:
            break
    return videos

def get_video_details(video_ids):
    details = []
    # YouTube API allows max 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        request = youtube.videos().list(
            part="contentDetails,snippet",
            id=",".join(batch)
        )
        response = request.execute()
        for item in response.get("items", []):
            duration = isodate.parse_duration(item["contentDetails"]["duration"]).total_seconds()
            if duration < 10:  # Filter videos shorter than 10 seconds
                details.append({
                    "videoId": item["id"],
                    "title": item["snippet"]["title"],
                    "duration": duration,
                    "url": f"https://www.youtube.com/watch?v={item['id']}"
                })
    return details

def main():
    print("Fetching playlists...")
    playlists = get_playlists(CHANNEL_ID)
    print(f"Found {len(playlists)} lesson review playlists.")

    all_videos = []
    for playlist in playlists:
        print(f"\nFetching videos from playlist: {playlist['title']}")
        video_ids = get_videos_from_playlist(playlist["id"])
        print(f"  Found {len(video_ids)} videos in this playlist.")
        short_videos = get_video_details(video_ids)
        print(f"  {len(short_videos)} videos shorter than 10 seconds.")
        all_videos.extend(short_videos)

    # Save results to JSON
    with open("asl_data/aslu_lesson_review_videos.json", "w") as f:
        json.dump(all_videos, f, indent=2)

    print(f"\nTotal short videos collected: {len(all_videos)}")
    print("Saved to aslu_lesson_review_videos.json")

if __name__ == "__main__":
    main()
