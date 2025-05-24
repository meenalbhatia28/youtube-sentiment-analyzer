import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_comments(video_id, max_comments=100):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []

    next_page_token = None
    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": snippet["authorDisplayName"],
                "text": snippet["textDisplay"],
                "published_at": snippet["publishedAt"]
            })

            if len(comments) >= max_comments:
                break

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return pd.DataFrame(comments)

# Run as script
if __name__ == "__main__":
    video_url = input("Paste YouTube video URL: ")
    video_id = video_url.split("v=")[-1].split("&")[0]
    df = get_comments(video_id)
    df.to_csv("data/comments.csv", index=False)
    print("✅ Saved to data/comments.csv")
